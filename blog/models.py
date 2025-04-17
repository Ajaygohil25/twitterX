import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by', blank=True, null=True)

    class Meta:
        abstract = True

class Post(TimeStampedModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('user-profile')

class Media(models.Model):
    file = models.FileField(upload_to="blog_media/", blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    @property
    def file_url(self):
        if self.file:
            return self.file.url

