from app.db.session import create_session
from sqlalchemy import select


class BaseOperator:

    async def upsert(self, objs, model, by_field=None, update_fields=None):
        raise NotImplementedError()

    async def save(self, obj):
        async with self.session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def update(self, model, pk, new_values):
        async with self.session() as session:
            obj = await session.get(model, pk)
            if obj:
                for k, v in new_values.items():
                    setattr(obj, k, v)
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
            return obj

    async def all(self, model, *filters):
        stmt = select(model).where(*filters)
        result = await self.select(stmt)
        return result.all()

    async def get(self, model, *filters):
        stmt = select(model).where(*filters)
        result = await self.select(stmt)
        return result.first()

    async def select(self, stmt, scalars=True):
        async with self.session() as session:
            result = await session.execute(stmt)
            if scalars:
               return result.scalars()
            return result

    def session(self):
        return create_session()
