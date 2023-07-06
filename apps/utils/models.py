import uuid

from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models


# Create your models here.
class AppQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class AppManager(models.Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db).exclude(is_deleted=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = AppManager()
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        """
        Soft delete
        """
        self.is_deleted = True
        self.save()


class GeoLocationModel(BaseModel):
    class Meta:
        abstract = True

    latitude = models.FloatField()
    longitude = models.FloatField()
    point = PointField(srid=4326, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.point = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)


class Dummy(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['name', 'is_deleted']


class GeoLocation(GeoLocationModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['id', 'is_deleted']
