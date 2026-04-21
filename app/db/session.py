from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.db_url, echo=settings.SQL_DEBUG)

create_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with create_session() as session:
        yield session


async def exec_in_session(statement, *args):
    async with create_session() as db:
        await db.execute(statement, *args)
        await db.commit()


SessionDep = Annotated[AsyncSession, Depends(get_db)]
