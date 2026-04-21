from datetime import datetime
from importlib import import_module

from sqlmodel import SQLModel, Field, DateTime, func

from app.core.config import settings
from app.models.statement.base import BaseStatement


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    deleted: bool = Field(default=False, nullable=True)
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': func.now(),
            'nullable': False,
        },
    )
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': func.now(),
            'nullable': False,
            'onupdate': func.now(),
        },
    )

    @classmethod
    def stmt(cls) -> BaseStatement:
        stmt_module = f'app.models.statement.{settings.db_type}'
        return import_module(stmt_module).Statement(cls)
