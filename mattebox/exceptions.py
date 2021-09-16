import json


class MatteBOXException(Exception):
    def __init__(self, e: Exception) -> None:
        super().__init__(json.loads(str(e))["errorMessage"])


class RecordingException(MatteBOXException):
    pass
