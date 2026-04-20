from datetime import datetime

from sqlmodel import SQLModel, Field, Column, DateTime, DATETIME, func


class BaseModel(SQLModel):

    id: int = Field(primary_key=True)
    deleted: bool = Field(default=False, nullable=True)
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            'nullable': False,
        },
    )
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': func.now(),
            'nullable': False,
            'onupdate': func.now(),
        }
    )
