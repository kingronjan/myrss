from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.crud.base import operator
from app.models.feed import Feed, FeedSource


async def create_feeds(feeds):
    await operator.upsert(feeds, Feed, by_field=Feed.id)


async def get_sources() -> list[FeedSource]:
    return await operator.all(FeedSource)


async def get_source(*filters) -> FeedSource | None:
    return await operator.get(FeedSource, *filters)


async def get_source_by_id(source_id: int) -> FeedSource | None:
    return await get_source(FeedSource.id == source_id)


async def create_source(url, description) -> FeedSource:
    source = FeedSource(url=url, description=description)
    return await operator.save(source)


async def update_source(source_id: int, url: str | None, description: str | None) -> None:
    new_values = {}
    if url:
        new_values['url'] = url
    if description:
        new_values['description'] = description
    if not new_values:
        return None
    return await operator.update(FeedSource, source_id, new_values)


async def get_feeds(source_id: int) -> list[Feed]:
    return await operator.all(Feed, Feed.source_id == source_id)


async def get_unsent_feeds():
    stmt = select(FeedSource, Feed).where(Feed.source_id == FeedSource.id)
    stmt = stmt.where(Feed.is_sent == False)
    stmt = stmt.order_by(Feed.source_id, Feed.published.desc())
    result = await operator.select(stmt, scalars=False)
    return result.all()
