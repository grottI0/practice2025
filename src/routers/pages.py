from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from settings import settings


router = APIRouter()


@router.get('/')
def index():
    with open(settings.INDEX_HTML_PATH) as file:
        return HTMLResponse(file.read())
