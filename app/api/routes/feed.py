from fastapi.background import BackgroundTasks

from app.exceptions import RecordNotFoundError
from app.services.feed import sync_feeds
from app.api.routes.route import APIRouter
from app.api import response
from app.models.feed import Feed, FeedSource
from app.db.session import SessionDep

router = APIRouter(
    prefix="/feed",
)


@router.get("/")
async def get_source_feeds(db: SessionDep, source_id: int):
    stmt = Feed.stmt().select().where(Feed.source_id == source_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/sources")
async def get_sources(db: SessionDep):
    stmt = FeedSource.stmt().select()
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/source/add")
async def add_source(db: SessionDep, url: str, description: str | None = None):
    source = FeedSource(url=url, description=description)
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source


@router.put("/source/{source_id}")
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


@router.delete("/source/{source_id}")
async def delete_source(
    db: SessionDep,
    source_id: int,
):
    stmt = FeedSource.stmt().delete().where(FeedSource.id == source_id)
    await db.execute(stmt)
    await db.commit()
    return response.success(message="Source deleted successfully")


@router.post("/source/sync")
async def sync_source(db: SessionDep, source_id: int, tasks: BackgroundTasks):
    stmt = FeedSource.stmt().select().where(FeedSource.id == source_id)
    result = await db.execute(stmt)
    source = result.scalars().first()
    if source is None:
        raise RecordNotFoundError()
    tasks.add_task(sync_feeds, source)
    return response.success(message="Task created successfully")
