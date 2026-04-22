import sqlalchemy as sa


class BaseDialect:
    def select(self, *args):
        return sa.select(*args)

    def insert(self, *args):
        return sa.insert(*args)

    def update(self, *args):
        return sa.update(*args)

    def delete(self, *args):
        return sa.delete(*args)

    def upsert(self, entity, by_field=None, update_fields=None):
        raise NotImplementedError()
