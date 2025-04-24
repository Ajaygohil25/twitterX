from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import comment
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.form import MediaForm, CommentForm
from blog.models import Post, Media, Like, Comment
from users.models import Following


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/home.html'
    ordering = ['-created_at']
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_likes =  Like.objects.filter(user = self.request.user).values_list('post_id', flat=True)
        context['liked_posts'] = user_likes

        context["following_users"] = (Following.objects.filter(follower_user=self.request.user).
                                      values_list('following_user_id',flat=True))

        context["login_user"] = self.request.user
        # breakpoint()
        if self.request.POST:
            context['comment_form'] = CommentForm(self.request.POST)
        else:
            context['comment_form'] = CommentForm()

        return context


class FollowingUserListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/home.html"
    paginate_by = 3

    def get_queryset(self):
        following_users = Following.objects.filter(
            follower_user=self.request.user
        ).values_list('following_user', flat=True)

        posts = Post.objects.filter(user_id__in=following_users).order_by('-created_at')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["login_user"] = self.request.user

        user_likes = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context['liked_posts'] = user_likes

        context["following_users"] = Following.objects.filter(
            follower_user=self.request.user
        ).values_list('following_user', flat=True)

        # Comment form
        if self.request.POST:
            context['comment_form'] = CommentForm(self.request.POST)
        else:
            context['comment_form'] = CommentForm()
        return context

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_likes = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context['liked_posts'] = user_likes

        post = self.get_object()
        if self.request.POST:
            context['comment_form'] = CommentForm(self.request.POST)
        else:
            context['comment_form'] = CommentForm()
            context["all_comments"] = post.comment_set.all()

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['media_form'] = MediaForm(self.request.POST, self.request.FILES)
        else:
            context['media_form'] = MediaForm()

        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.created_by = self.request.user

        response = super().form_valid(form)

        # Handle media form
        media_files = self.request.FILES.getlist('file')
        if media_files:
            for f in media_files:
                Media.objects.create(post=self.object, file=f)

        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()

        if self.request.user != post.user_id:
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['media_form'] = MediaForm(self.request.POST, self.request.FILES)
        else:
            context['media_form'] = MediaForm()

        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.created_by = self.request.user

        response = super().form_valid(form)

        # Handle media form
        media_files = self.request.FILES.getlist('file')
        if media_files:
            for f in media_files:
                Media.objects.create(post=self.object, file=f)

        return response

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user != post.user_id:
            return False
        return True

class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        liked = Like.objects.filter(user=request.user, post=post).first()

        if liked:
            liked.delete() # unlike the post if instance exists in database
            is_liked = False
        else:
            like = Like(user=request.user, post=post, created_by=request.user)
            like.save()
            is_liked = True

        # Send the update button
        html = render_to_string("partials/like_button.html",
                                {
                                    "post": post,
                                    "is_liked": is_liked,
                                },request=request)

        return HttpResponse(html)
        # return JsonResponse({
        #     'is_liked': is_liked,
        #     "likes": post.like_set.count(),
        # })


class CommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        comment_text = request.POST.get('comment')

        if comment_text:
            comment = Comment(post=post, comment=comment_text, commented_by=request.user, created_by=request.user)
            comment.save()

        html = render_to_string("partials/comment_button.html",
                                {
                                    "post": post,
                                    "comment_form": CommentForm(),
                                }, request=request)

        return HttpResponse(html)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = "/"

    def test_func(self):
        comment = self.get_object()
        if self.request.user != comment.commented_by and self.request.user != comment.post.user_id:
            return False
        return True

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    success_url = "user-profile"
    fields = ['comment']

    def test_func(self):
        comment = self.get_object()
        if self.request.user != comment.commented_by and self.request.user != comment.post.user_id:
            return False
        return True

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs["pk"])
        comment_text = request.POST.get('comment')
        if comment_text:
            comment.comment = comment_text
            comment.save()
            messages.success(request, f'Comment updated successfully!')

        return redirect('blog-detail', pk=comment.post.id)



def about(request):
    return render(request, 'blog/about.html', {"title": "About"})