from sqlalchemy.dialects.sqlite import insert

from app.db.dialects.base import BaseDialect


class Dialect(BaseDialect):
    def upsert(self, entity, by_field=None, update_fields=None):
        stmt = insert(entity)
        index_elements = [by_field]

        if update_fields:
            set_ = {f: getattr(stmt.excluded, f) for f in update_fields}
            return stmt.on_conflict_do_update(index_elements=index_elements, set_=set_)

        return stmt.on_conflict_do_nothing(index_elements=index_elements)
