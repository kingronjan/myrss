class UnifiedError(Exception):
    message = None

    def __init__(self):
        if self.message is None:
            message = self.__class__.__name__
        else:
            message = self.message
        super().__init__(message)


class RecordNotFoundError(UnifiedError):
    pass
