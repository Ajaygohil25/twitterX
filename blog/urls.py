from django.urls import path
from .views import home, about, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
       PostLikeView

urlpatterns = [
       path('',PostListView.as_view() , name="blog-home"),
       path('about', about, name="blog-about" ),
       path('post/<int:pk>/',PostDetailView.as_view() , name="blog-detail"),
       path('post/create', PostCreateView.as_view() , name="blog-create"),
       path('post/<int:pk>/update',PostUpdateView.as_view() , name="blog-update"),
       path('post/<int:pk>/delete',PostDeleteView.as_view() , name="blog-delete"),
       path('post/<int:pk>/like',PostLikeView.as_view(),  name='blog-like'),
]