import os
import sqlite3
from typing import Generator

import cv2
import numpy as np
import supervision
from inference import get_model

from queries import UPDATE
from settings import settings


model = get_model(settings.ROBOFLOW_MODEL, api_key=settings.ROBOFLOW_TOKEN)
bounding_box_annotator = supervision.BoundingBoxAnnotator(color=supervision.Color(255, 0, 0), thickness=3)


def process_frame(frame: np.array) -> tuple[np.array, bool]:
    result = model.infer(frame)[0]
    detections = supervision.Detections.from_inference(result)
    detected = settings.BALL_CLASS_ID in detections.class_id
    return bounding_box_annotator.annotate(
        scene=frame.copy(),
        detections=detections
    ), detected

def generate_frames(video_path: str) -> Generator[bytes, None, None]:
    cap = cv2.VideoCapture(video_path)
    total, detected = 0, 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed, is_ball_detected = process_frame(frame)
        ret, buf = cv2.imencode('.jpg', processed)
        if not ret:
            continue

        total += 1
        if is_ball_detected:
            detected += 1

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")

    cap.release()
    os.remove(video_path)
    print(f"{video_path} is processed and removed")
    with sqlite3.connect(settings.DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            UPDATE,
            (total, detected, round(detected / total * 100, 2), video_path),
        )
        cur.close()
