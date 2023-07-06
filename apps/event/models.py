import uuid

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models

from apps.user.models import User
from apps.utils.models import GeoLocationModel


# Create your models here.
class Event(GeoLocationModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_host')
    name = models.CharField(max_length=100)
    description = models.TextField()
    preparation = models.TextField()
    image = CloudinaryField('image', null=True, blank=True, default=None)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    staffs = models.ManyToManyField(User, related_name='events_staff')
    supports = models.ManyToManyField(User, related_name='events_support')
    is_verified = models.BooleanField(default=False)

    class Meta:
        unique_together = ['id', 'is_deleted']
        ordering = ['start_date']

    @property
    def image_url(self):
        return f'https://res.cloudinary.com/{settings.CLOUDINARY_CLOUD_NAME}/{self.image}' if self.image else ''

    @property
    def total_participant(self):
        return len(self.joined_users.all())

    def __str__(self):
        return self.name
