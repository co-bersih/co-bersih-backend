import uuid

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models

from apps.user.models import User
from apps.utils.models import BaseModel


# Create your models here.

class Report(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    image = CloudinaryField('image', null=True, blank=True, default=None)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_events')
    reported_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ['id', 'is_deleted']
        ordering = ['-reported_date']

    @property
    def image_url(self):
        return f'https://res.cloudinary.com/{settings.CLOUDINARY_CLOUD_NAME}/{self.image}' if self.image else ''