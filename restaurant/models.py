import uuid
from django.db import models


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number}"