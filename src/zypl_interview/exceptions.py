class CustomBaseError(ValueError):
    def __init__(self, msg: str, status_code: int):
        self.message = msg
        self.status_code = status_code
