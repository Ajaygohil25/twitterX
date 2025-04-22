from django.urls import path
from .views import about, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
       PostLikeView, CommentView, CommentDeleteView, CommentUpdateView, FollowingUserListView

urlpatterns = [
       path('',PostListView.as_view() , name="blog-home"),
       path('about', about, name="blog-about" ),
       path('post/<int:pk>/',PostDetailView.as_view() , name="blog-detail"),
       path('post/create', PostCreateView.as_view() , name="blog-create"),
       path('post/<int:pk>/update',PostUpdateView.as_view() , name="blog-update"),
       path('post/<int:pk>/delete',PostDeleteView.as_view() , name="blog-delete"),
       path('post/<int:pk>/like',PostLikeView.as_view(),  name='blog-like'),
       path("post/<int:pk>/comment", CommentView.as_view(), name='blog-comment'),
       path("post/comment/<int:pk>/delete", CommentDeleteView.as_view(), name='blog-comment-delete'),
       path("post/comment/<int:pk>/update", CommentUpdateView.as_view(), name='blog-comment-update'),

       path("following-feed", FollowingUserListView.as_view(), name="following-feed")
]