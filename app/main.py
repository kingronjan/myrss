import logging
from urllib.request import Request

from starlette.exceptions import HTTPException
import fastapi

from app.api.endpoints import feed, email
from app.api import response
from app.core.config import settings

app = fastapi.FastAPI()

logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT,)

# routers
app.include_router(feed.router)
app.include_router(email.router)

# exception handlers
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return response.failed(message=str(exc))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return response.failed(message=str(exc), status_code=exc.status_code)


@app.get('/')
async def index():
    return {'message': 'Hello World'}
