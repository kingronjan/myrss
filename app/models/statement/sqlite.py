from sqlalchemy.dialects.sqlite import insert

from app.models.statement.base import BaseStatement


class Statement(BaseStatement):
    def upsert(self, by_field=None, update_fields=None):
        stmt = insert(self.model)
        index_elements = [by_field or self.model.id]

        if update_fields:
            set_ = {f: getattr(stmt.excluded, f) for f in update_fields}
            return stmt.on_conflict_do_update(index_elements=index_elements, set_=set_)

        return stmt.on_conflict_do_nothing(index_elements=index_elements)
