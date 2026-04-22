from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.dialects import get_dialect

engine = create_async_engine(settings.db_url, echo=settings.SQL_DEBUG)


class DatabaseSession(AsyncSession):
    dialect = get_dialect()

    async def delete_by_pk(self, entity, pk):
        stmt = self.dialect.delete(entity).where(entity.id == pk)
        await self.execute(stmt)
        await self.commit()

    async def update_by_pk(self, entity, pk, values):
        stmt = self.dialect.update(entity).where(entity.id == pk).values(**values)
        await self.execute(stmt)
        await self.commit()

    async def save(self, instance):
        self.add(instance)
        await self.commit()
        await self.refresh(instance)
        return instance

    async def set_values(self, instance, **values):
        for k, v in values.items():
            setattr(instance, k, v)
        model = instance.__class__
        stmt = (
            self.dialect.update(model).where(model.id == instance.id).values(**values)
        )
        await self.execute(stmt)
        await self.commit()


create_session: async_sessionmaker[DatabaseSession] = sessionmaker(
    engine, class_=DatabaseSession, expire_on_commit=False
)


async def get_db() -> AsyncIterator[DatabaseSession]:
    async with create_session() as session:
        yield session


SessionDep = Annotated[DatabaseSession, Depends(get_db)]
