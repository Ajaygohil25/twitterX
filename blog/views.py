from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.form import MediaForm
from blog.models import Post, Media, Like


def home(request):
    posts = Post.objects.all()
    contexts = {
        "posts": posts,
    }
    return render(request, 'blog/home.html', context=contexts)

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
        return context

class PostDetailView(DetailView):
    model = Post

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

class PostLikeView(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        liked = Like.objects.filter(user=request.user, post=post).first()
        if liked:
            liked.delete() # unlike the post if instance exists in database
        else:
            like = Like(user=request.user, post=post, created_by=request.user)
            like.save()
        return redirect('blog-home')
def about(request):
    return render(request, 'blog/about.html', {"title": "About"})