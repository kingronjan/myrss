from typing import TypeVar, Generic, Any, Callable

from reprlib import Repr


class MyRepr(Repr):
    def repr_FeedParserDict(self, x, level):  # noqa
        return self.repr_dict(x, level)


class LazyRepr:
    def __init__(self, obj, **kwargs):
        self.obj = obj
        self.kwargs = kwargs

    def __str__(self):
        repr_ = MyRepr(**self.kwargs)
        return repr_.repr(self.obj)


T = TypeVar("T")


class cached_classpriority(Generic[T]):  # noqa
    def __init__(self, func: Callable[[Any], T]):
        self.func = func
        self._result = None

    def __get__(self, instance: Any, owner: type[Any]) -> T:
        if self._result is None:
            self._result = self.func(instance)
        return self._result
