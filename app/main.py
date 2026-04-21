import logging
from urllib.request import Request

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from app.api import response
from app.api.routes import feed, email, feedsource
from app.core.config import settings

app = fastapi.FastAPI()

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
)

# routers
app.include_router(feed.router)
app.include_router(email.router)
app.include_router(feedsource.router)

# frontend
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(
    CORSMiddleware,
    # 匹配 http://localhost:任何数字 和 http://127.0.0.1:任何数字
    allow_origin_regex=r'https?://(localhost|127\.0\.0\.1)(:\d+)?',
    allow_credentials=True,  # 使用正则时，这里可以设为 True
    allow_methods=['*'],
    allow_headers=['*'],
)


# exception handlers
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return response.failed(message=str(exc))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return FileResponse('static/index.html')
    return response.failed(message=str(exc), status_code=exc.status_code)


@app.get('/')
async def index():
    return FileResponse('static/index.html')
