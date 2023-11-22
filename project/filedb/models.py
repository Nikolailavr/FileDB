import enum
import uuid
from collections import Counter

from django.db import models


class FileType(str, enum.Enum):
    Type_1 = 'type1'
    Type_2 = 'type2'


class File(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['type']),
            models.Index(fields=['vendor']),
            models.Index(fields=['date_revision']),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    type = models.CharField(max_length=10,
                            db_index=True,
                            choices=[(item.value, item.name) for item in FileType])
    vendor = models.CharField(max_length=50, db_index=True)
    date_revision = models.DateField(db_index=True)
    extra_field = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.vendor}"

    @classmethod
    def cleanup_on_stop_app(cls):
        for item in cls.objects.values('vendor').distinct():
            types = Counter(
                cls.objects.filter(vendor=item['vendor']).
                values_list('type', flat=True)
            )
            if types.most_common()[0][1] > 1:
                cls.objects.filter(vendor=item['vendor']).delete()
