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

    def delete(self):
        """
        Soft delete
        """
        self.is_deleted = True
        self.save()


class Dummy(BaseModel):
    class Meta:
        unique_together = ['name', 'is_deleted']

    name = models.CharField(max_length=100)
