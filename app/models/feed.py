from datetime import datetime
from typing import Optional

from sqlmodel import Field, TEXT

from app.models.base import BaseModel
from app.core.enums import TaskStatus


class FeedSource(BaseModel, table=True):
    url: str = Field(max_length=255, nullable=True, unique=True)
    description: str = Field(max_length=255, nullable=True)
    sync_status: TaskStatus = Field(nullable=True, default=TaskStatus.UNSET)
    sync_msg: str = Field(max_length=500, nullable=True)

    @property
    def desc(self):
        return self.description or self.url


class Feed(BaseModel, table=True):
    id: Optional[str] = Field(max_length=255, nullable=False, primary_key=True)
    source_id: int = Field(nullable=False, index=True)
    title: str = Field(max_length=500, nullable=False)
    link: str = Field(max_length=500, nullable=False)
    summary: Optional[str] = Field(sa_type=TEXT, nullable=True)
    published: datetime = Field(nullable=False)
    is_sent: Optional[bool] = Field(nullable=False, default=False)
    is_read: Optional[bool] = Field(nullable=False, default=False)

    @property
    def published_str(self):
        return self.published.strftime('%Y-%m-%d')
