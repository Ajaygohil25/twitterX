from django import forms
from django.forms.widgets import ClearableFileInput

from blog.models import Media, Comment


class MediaForm(forms.ModelForm):
    file = forms.FileField(
        widget=ClearableFileInput(attrs={'allow_multiple_selected': True}),
        required=False
    )

    class Meta:
        model = Media
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        }


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, max_length=50)

    class Meta:
        model = Comment
        fields = ['comment']

class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea, max_length=50)

    class Meta:
        model = Comment
        fields = ['reply']