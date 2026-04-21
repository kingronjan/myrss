from email.mime.text import MIMEText
from collections import defaultdict
from datetime import datetime

import aiosmtplib

from app.core.config import settings
from app.db.session import SessionDep
from app.models.feed import Feed, FeedSource


async def send(subject, message):
    # 构建邮件对象
    if not isinstance(message, MIMEText):
        message = MIMEText(message, "plain", "utf-8")

    message["From"] = settings.MAIL_SENDER
    message["To"] = settings.MAIL_RECEIVER
    message["Subject"] = subject

    await aiosmtplib.send(
        message,
        hostname=settings.MAIL_SMTP_SERVER,
        port=settings.MAIL_SMTP_PORT,
        username=settings.MAIL_SENDER,
        password=settings.MAIL_PASSWORD,
        use_tls=True,
    )


async def send_feeds(db: SessionDep):
    stmt = Feed.stmt().select(FeedSource, Feed).where(Feed.source_id == FeedSource.id)
    stmt = stmt.where(Feed.is_sent == False)
    stmt = stmt.order_by(Feed.source_id, Feed.published.desc())

    feeds = await db.execute(stmt)
    feeds = feeds.all()

    message = make_feed_email_message(feeds)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"[MyRSS] New articles from {date} "
    await send(subject, message)


def make_feed_email_message(feeds):
    messages = defaultdict(list)

    for source, feed in feeds:
        messages[source.desc].append(feed)

    content = [
        "<html>",
        "<body>",
        "<h2>Here are some new articles for you:</h2>",
    ]

    for desc, feeds in messages.items():
        content.append(f"<p><b>{desc}</b></p>")
        content.append("<ul>")
        for feed in feeds:
            content.append(
                f'<li><a href="{feed.link}">[{feed.published_str}] {feed.title}</a></li>'
            )
        content.append("</ul>")

    content.append("</body>")
    content.append("</html>")

    content = "".join(content)
    return MIMEText(content, "html", "utf-8")
