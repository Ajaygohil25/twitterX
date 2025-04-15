from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Post

def home(request):
    posts  = Post.objects.all()
    contexts = {
        "posts": posts,
    }
    return render(request, 'blog/home.html', context=contexts)

def about(request):
    return render(request, 'blog/about.html', {"title": "About"})