from fastapi import BackgroundTasks

from app.api import response
from app.api.routes.route import APIRouter
from app.db.session import SessionDep
from app.exceptions import RecordNotFoundError
from app.models.feed import FeedSource
from app.services.feed import sync_feeds

router = APIRouter(
    prefix="/feed-source",
)


@router.get("/")
async def get_sources(db: SessionDep):
    stmt = FeedSource.stmt().select()
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/add")
async def add_source(db: SessionDep, url: str, description: str | None = None):
    source = FeedSource(url=url, description=description)
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source


@router.put("/{source_id}")
async def update_source(
    db: SessionDep,
    source_id: int,
    url: str | None = None,
    description: str | None = None,
):
    stmt = (
        FeedSource.stmt()
        .update()
        .where(FeedSource.id == source_id)
        .values(url=url, description=description)
    )
    await db.execute(stmt)
    await db.commit()
    return response.success(message="Source updated successfully")


@router.delete("/{source_id}")
async def delete_source(
    db: SessionDep,
    source_id: int,
):
    stmt = FeedSource.stmt().delete().where(FeedSource.id == source_id)
    await db.execute(stmt)
    await db.commit()
    return response.success(message="Source deleted successfully")


@router.post("/sync")
async def sync_source(db: SessionDep, source_id: int, tasks: BackgroundTasks):
    stmt = FeedSource.stmt().select().where(FeedSource.id == source_id)
    result = await db.execute(stmt)
    source = result.scalars().first()
    if source is None:
        raise RecordNotFoundError()
    tasks.add_task(sync_feeds, source)
    return response.success(message="Task created successfully")


@router.get("/sync-status")
async def sync_status(db: SessionDep, source_id: int):
    stmt = FeedSource.stmt().select().where(FeedSource.id == source_id)
    result = await db.execute(stmt)
    source = result.scalars().first()
    if source is None:
        raise RecordNotFoundError()
    return source
