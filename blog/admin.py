from django.contrib import admin

from blog.models import Post, Media

# Register your models here.
admin.site.register(Post)
admin.site.register(Media)