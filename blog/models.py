from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)s_created_by'  # dynamic: will be like 'comment_created_by'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)s_updated_by',
        blank=True, null=True
    )

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

    def get_like_count(self):
        return self.like_set.count()

    def get_comment_count(self):
        return self.comment_set.count()

    def get_all_comments(self):
        return self.comment_set.all()

    def get_queryset(self):
        return Post.objects.filter(user_id=self.user_id).order_by('-created_at').all()

class Media(models.Model):
    file = models.FileField(upload_to="blog_media/", blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return None

class Like(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_by')

class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def get_all_replies(self):
        return self.reply_set.all()

class Reply(TimeStampedModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField(blank=False, null=False)
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replied_by')