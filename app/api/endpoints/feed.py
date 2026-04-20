from fastapi.background import BackgroundTasks

from app.crud import feed
from app.exceptions import RecordNotFoundError
from app.services.feed import sync_feeds
from app.api.route import APIRouter
from app.api import response

router = APIRouter(
    prefix='/feed',
)

@router.post('/source/add')
async def add_source(url: str, description: str | None = None):
    return await feed.create_source(url, description)


@router.put('/source/{source_id}')
async def update_source(source_id: int, url: str | None = None, description: str | None = None):
    return await feed.update_source(source_id, url, description)


@router.get('/sources')
async def get_sources():
    return await feed.get_sources()


@router.get('/')
async def get_source_feeds(source_id: int):
    return await feed.get_feeds(source_id)


@router.post('/source/sync')
async def sync_source(source_id: int, tasks: BackgroundTasks):
    source = await feed.get_source_by_id(source_id)
    if source is None:
        raise RecordNotFoundError()
    tasks.add_task(sync_feeds, source)
    return response.success(message='Task created successfully')
