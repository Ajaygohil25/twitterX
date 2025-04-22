from django.contrib.auth.models import User
from django.db import models
from blog.models import TimeStampedModel

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics")
    bio = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Following(TimeStampedModel):
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')  # the one who follows others
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')  # the one being followed
