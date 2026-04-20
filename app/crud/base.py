from importlib import import_module

from app.core.config import settings


def get_operator():
    module_name = f'app.crud.operators.{settings.db_type}'
    module = import_module(module_name)
    return module.Operator()

operator = get_operator()
