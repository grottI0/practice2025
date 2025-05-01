import sqlite3

import uvicorn
from fastapi import FastAPI

from queries import CREATE
from routers import pages_router, video_router
from settings import settings


app = FastAPI()
app.include_router(video_router)
app.include_router(pages_router)

if __name__ == "__main__":
    with sqlite3.connect(settings.DB_PATH) as conn:
        conn.execute(CREATE)
    uvicorn.run("main:app", reload=True, log_level='info')
