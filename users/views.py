from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView
from blog.models import Post
from users.form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created successfully! Now please login !')
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, "users/registration.html", {"form": form})

class ProfileDetailView(LoginRequiredMixin, FormView):
    model = User
    template_name = "users/profile.html"
    context_object_name = 'posts'
    success_url = 'user-profile'
    ordering = ['-created_at']
    paginate_by = 3


    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        post_form = ProfileUpdateForm(instance=request.user.profile)
        posts = Post.objects.filter(user_id=self.request.user).order_by('-created_at').all()
        return self.render_to_response({"user_form": user_form, "post_form": post_form, "posts": posts})

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        post_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and post_form.is_valid():
            user_form.save()
            post_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile')
        else:
            messages.error(request, f'Error updating your account!')
            return redirect('user-profile')

