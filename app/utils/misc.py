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
