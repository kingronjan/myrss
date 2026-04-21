import logging
from datetime import datetime
from time import mktime

import httpx
import feedparser

from app.models.feed import Feed, FeedSource
from app.utils.misc import LazyRepr
from app.db.session import SessionDep

logger = logging.getLogger(__name__)


async def fetch_feeds(source: FeedSource) -> list[Feed]:
    logger.debug(f"Fetching feeds for {source}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(source.url)
        result = feedparser.parse(resp.text)

    feeds = []

    for entry in result.entries:
        logger.debug("Fetched entry: %s", LazyRepr(entry, maxstring=20, maxdict=20))
        published = datetime.fromtimestamp(mktime(entry.published_parsed))
        feed = Feed(
            title=entry.title,
            link=entry.link,
            id=entry.id,
            summary=entry.summary,
            source_id=source.id,
            published=published,
        )
        feeds.append(feed)

    return feeds


async def sync_feeds(db: SessionDep, source: FeedSource) -> None:
    feeds = await fetch_feeds(source)
    stmt = Feed.stmt.upsert(feeds)
    await db.execute(stmt)
    await db.commit()
