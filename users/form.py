from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from users.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    bio = forms.CharField(widget=forms.Textarea, max_length=250)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile = user.profile
            profile.bio = self.cleaned_data['bio']
            if self.cleaned_data.get('image'):
                profile.image = self.cleaned_data['image']
            profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, max_length=250, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'image']