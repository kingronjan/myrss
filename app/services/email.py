import asyncio
from email.mime.text import MIMEText
from collections import defaultdict
from datetime import datetime

import aiosmtplib

from app.core.config import settings
from app.crud.feed import get_unsent_feeds


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


async def send_feeds():
    feeds = await get_unsent_feeds()
    message = make_feed_email_message(feeds)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f'[MyRSS] New articles from {date} '
    await send(subject, message)


def make_feed_email_message(feeds):
    messages = defaultdict(list)

    for source, feed in feeds:
        messages[source.desc].append(feed)

    content = [
        '<html>',
        '<body style="font-family: Consola;">',
        '<h2>Here are some new articles for you:</h2>',
    ]

    for desc, feeds in messages.items():
        content.append(f'<p><b>{desc}</b></p>')
        content.append('<ul>')
        for feed in feeds:
            content.append(f'<li><a href="{feed.link}">[{feed.published_str}] {feed.title}</a></li>')
        content.append('</ul>')

    content.append('</body>')
    content.append('</html>')

    content = ''.join(content)
    return MIMEText(content, "html", "utf-8")
