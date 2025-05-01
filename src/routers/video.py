import csv
import io
import os
import sqlite3
from tempfile import NamedTemporaryFile
from time import time

from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.routing import APIRouter

from queries import SELECT_ALL, SELECT_VIDEO, UPLOAD_VIDEO
from service import generate_frames
from settings import settings
from utils import convert_timestamp


router = APIRouter()


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    temp_file = NamedTemporaryFile(delete=False)
    video_path = temp_file.name

    with open(video_path, "wb") as f:
        f.write(await file.read())

    with sqlite3.connect(settings.DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(UPLOAD_VIDEO, (video_path, convert_timestamp(time()), file.filename))
        cursor.close()

    print(f"Saved {video_path} video")
    return JSONResponse({"video_id": video_path})


@router.get("/stream")
def stream_video(video_id: str): 
    if not os.path.exists(video_id):
        return JSONResponse({"error": "Video not found"}, status_code=404)

    return StreamingResponse(
        generate_frames(video_id),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.get("/stat")
def statistics(video_id: str):
    with sqlite3.connect(settings.DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_VIDEO, (video_id,))
        row = cursor.fetchone()
        cursor.close()

    return {
        "original_name": row[0],
        "timestamp": row[1],
        "total": row[2],
        "detected": row[3],
        "percent": row[4]
    }

@router.get("/report")
def report():
    with sqlite3.connect(settings.DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_ALL)
        description = cursor.description
        rows = cursor.fetchall()
        cursor.close()

    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=';')
    writer.writerow([
        d[0].replace("_", " ").capitalize() for d in description
    ])
    writer.writerows(rows)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=video_stats.csv"}
    )