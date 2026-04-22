from app.models.feed import Feed, FeedSource
from app.db.session import DatabaseSession


async def get_unsent_feeds(db: DatabaseSession):
    stmt = db.dialect.select(FeedSource, Feed).where(Feed.source_id == FeedSource.id)
    stmt = stmt.where(Feed.is_sent == False)
    stmt = stmt.order_by(Feed.source_id, Feed.published.desc())
    feeds = await db.execute(stmt)
    return feeds.all()


async def upsert_feeds(db: DatabaseSession, feeds: list[Feed]):
    stmt = db.dialect.upsert(Feed, by_field=Feed.id)
    await db.execute(stmt, feeds)
    await db.commit()
