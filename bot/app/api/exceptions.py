class BackendApiError(Exception):
    pass


class BackendUnauthorizedError(BackendApiError):
    pass


class BackendValidationError(BackendApiError):
    def __init__(self, payload):
        self.payload = payload
        super().__init__(str(payload))
