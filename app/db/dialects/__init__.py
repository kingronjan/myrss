from importlib import import_module

from app.core.config import settings
from app.db.dialects.base import BaseDialect


def get_dialect() -> BaseDialect:
    dialect_module = import_module(f'app.db.dialects.{settings.db_type}')
    return dialect_module.Dialect()
