from sqlalchemy.dialects.sqlite import insert

from app.crud.operators.base import BaseOperator
from app.db.session import create_session


class Operator(BaseOperator):

    async def upsert(self, objs, model, by_field=None, update_fields=None):
        async with create_session() as session:
            stmt = insert(model)
            index_elements = [by_field]
            if update_fields:
                set_ = {f: getattr(stmt.excluded, f) for f in update_fields}
                upsert_stmt = stmt.on_conflict_do_update(
                    index_elements=index_elements,
                    set_=set_
                )
            else:
                upsert_stmt = stmt.on_conflict_do_nothing(
                    index_elements=index_elements
                )
            await session.execute(upsert_stmt, objs)
            await session.commit()
