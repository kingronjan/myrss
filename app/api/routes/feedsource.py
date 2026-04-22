from fastapi import BackgroundTasks

from app.api import response
from app.api.routes.route import APIRouter
from app.db.session import SessionDep
from app.exceptions import RecordNotFoundError
from app.models.feed import FeedSource
from app.models.schemas import FeedSourceUpdate, FeedSourceCreate
from app.services.feed import sync_feeds

router = APIRouter(
    prefix='/feed-source',
)


@router.get('/')
async def get_sources(db: SessionDep):
    stmt = db.dialect.select(FeedSource).order_by(FeedSource.id.desc())
    result = await db.scalars(stmt)
    return result.all()


@router.post('/add')
async def add_source(db: SessionDep, source_in: FeedSourceCreate):
    source = FeedSource(**source_in.model_dump(exclude_unset=True))
    return await db.save(source)


@router.put('/{source_id}')
async def update_source(
    db: SessionDep,
    source_id: int,
    source_in: FeedSourceUpdate,
):
    values = source_in.model_dump(exclude_unset=True)
    await db.update_by_pk(FeedSource, source_id, values)
    return response.success(message='Source updated successfully')


@router.delete('/{source_id}')
async def delete_source(
    db: SessionDep,
    source_id: int,
):
    await db.delete_by_pk(FeedSource, source_id)
    return response.success(message='Source deleted successfully')


@router.post('/sync')
async def sync_source(db: SessionDep, source_id: int, tasks: BackgroundTasks):
    source = await db.get(FeedSource, source_id)
    if source is None:
        raise RecordNotFoundError()
    if source is None:
        raise RecordNotFoundError()
    tasks.add_task(sync_feeds, source)
    return response.success(message='Task created successfully')


@router.get('/sync-status')
async def sync_status(db: SessionDep, source_id: int):
    source = await db.get(FeedSource, source_id)
    if source is None:
        raise RecordNotFoundError()
    return source
