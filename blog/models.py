import uuid

from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by')

    class Meta:
        abstract = True
# class Media(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     media_url = models.URLField()


class Post(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # media_id = models.ForeignKey('Media', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
