from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):

    ROBOFLOW_TOKEN: str
    ROBOFLOW_MODEL: str = "soccerballdetector/1"
    DB_PATH: str = "../base.db"
    BALL_CLASS_ID: int = 0
    INDEX_HTML_PATH: str = "../html/index.html"


settings = AppSettings(_env_file="../.env")
