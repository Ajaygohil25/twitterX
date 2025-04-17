from django import forms
from django.forms.widgets import ClearableFileInput

from blog.models import Media


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
