import logging
from datetime import datetime
from time import mktime

import httpx
import feedparser

from app.models.feed import Feed, FeedSource
from app.utils.misc import LazyRepr
from app.db.session import exec_in_session
from app.core.enums import TaskStatus

logger = logging.getLogger(__name__)


async def fetch_feeds(source: FeedSource) -> list[Feed]:
    logger.debug(f'Fetching feeds for {source}')

    async with httpx.AsyncClient() as client:
        resp = await client.get(source.url)
        result = feedparser.parse(resp.text)

    feeds = []

    for entry in result.entries:
        logger.debug('Fetched entry: %s', LazyRepr(entry, maxstring=20, maxdict=20))
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


async def sync_feeds(source: FeedSource) -> None:
    try:
        stmt = FeedSource.stmt().update().values(sync_status=TaskStatus.RUNNING)
        await exec_in_session(stmt)

        feeds = await fetch_feeds(source)
        stmt = Feed.stmt().upsert()
        await exec_in_session(stmt, feeds)

        status = TaskStatus.SUCCESS
        msg = None

    except httpx.ConnectTimeout:
        status = TaskStatus.FAILED
        msg = 'Connection timeout'

    except Exception as e:
        logger.exception(f'Source {source.id} sync failed', exc_info=e)
        status = TaskStatus.FAILED
        msg = str(e)

    stmt = FeedSource.stmt().update().values(sync_status=status, sync_msg=msg)
    await exec_in_session(stmt)
