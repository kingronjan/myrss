from typing import TYPE_CHECKING

from app.db.session import create_session
from sqlalchemy import select, delete, update


if TYPE_CHECKING:
    from app.models.base import BaseModel as SQLModel
else:
    from sqlmodel import SQLModel


class BaseStatement:
    session = create_session

    def __init__(self, model: SQLModel) -> None:
        self.model = model
        self._default = (self.model,)

    def upsert(self, by_field=None, update_fields=None):
        raise NotImplementedError

    def select(self, *args):
        return select(*(args or self._default)).where(self.model.deleted == False)

    def delete(self, *args):
        return delete(*(args or self._default))

    def update(self, *args):
        return update(*(args or self._default))
