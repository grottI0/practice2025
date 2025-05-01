from datetime import datetime


def convert_timestamp(timestamp: float):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
