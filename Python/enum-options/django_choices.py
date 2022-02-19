from django.db import models


class HttpStatus(models.TextChoices):
    NOT_FOUND = 404
    SUCCESS = 200
    INTERNAL_SERVER_ERROR = 500
