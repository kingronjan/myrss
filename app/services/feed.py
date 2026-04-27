import logging
from datetime import datetime
from time import mktime
from urllib.parse import urljoin

import httpx
import feedparser
from bs4 import BeautifulSoup

from app.models.crud import upsert_feeds
from app.models.feed import Feed, FeedSource
from app.utils.misc import LazyRepr
from app.db.session import create_session
from app.core.enums import TaskStatus

logger = logging.getLogger(__name__)


async def sync_feeds(source: FeedSource) -> None:
    async with create_session() as db:
        await _sync_feeds(source, db)


async def _sync_feeds(source, db):
    try:
        await db.set_values(source, sync_status=TaskStatus.RUNNING)
        feeds = await fetch_feeds(source)
        await upsert_feeds(db, feeds)
        status = TaskStatus.SUCCESS
        msg = None

    except httpx.ConnectTimeout:
        status = TaskStatus.FAILED
        msg = 'Connection timeout'

    except Exception as e:
        logger.exception(f'Source {source.id} sync failed', exc_info=e)
        status = TaskStatus.FAILED
        msg = str(e)

    await db.set_values(source, sync_status=status, sync_msg=msg)


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
            content=_get_content(entry),
            source_id=source.id,
            published=published,
            cover_url=_get_rss_cover(entry),
        )
        feeds.append(feed)

    return feeds


def _get_content(entry: feedparser.FeedParserDict) -> str | None:
    # 3. 尝试从正文 (summary 或 content) 中解析第一张 <img>
    # 优先取 content，没有则取 summary
    try:
        return entry.content[0].value
    except KeyError:
        return entry.summary


def _get_rss_cover(entry):
    """
    按优先级获取 RSS 文章封面图
    1. media:content (Media RSS 扩展)
    2. enclosure (标准附件)
    3. og:image (如果有 link 且进行了二次抓取，这里暂不演示网络请求)
    4. 从正文 HTML 提取第一张图
    """

    # 1. 尝试从 media:content 获取 (常用于高质量源)
    if 'media_content' in entry:
        # 可能会有多个媒体资源，找类型为 image 的
        images = [
            m['url']
            for m in entry.media_content
            if 'image' in m.get('medium', '') or 'image' in m.get('type', '')
        ]
        if images:
            return images[0]

    # 2. 尝试从 enclosure 获取
    if 'enclosures' in entry:
        images = [
            e['href'] for e in entry.enclosures if e.get('type', '').startswith('image')
        ]
        if images:
            return images[0]

    # 3. 尝试从正文 (summary 或 content) 中解析第一张 <img>
    # 优先取 content，没有则取 summary
    html_content = ''
    if 'content' in entry:
        html_content = entry.content[0].value
    elif 'summary' in entry:
        html_content = entry.summary

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            return urljoin(entry.link, img_tag['src'])

    return None
