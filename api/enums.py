from django.db import models

class ContentLanguageStatus(models.IntegerChoices):
    WAITING = 0, 'Waiting'
    PROCESSING = 1, 'Processing'
    COMPLETED = 2, 'Completed'
    FAILED = 3, 'Failed'
