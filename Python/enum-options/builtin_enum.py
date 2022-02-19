from enum import Enum


class HttpStatus(Enum):
    NOT_FOUND = 404
    SUCCESS = 200
    INTERNAL_SERVER_ERROR = 500
