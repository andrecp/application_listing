from django import forms
from .models import Application


class CreateApplicationForm(forms.ModelForm):

    class Meta(object):
        model = Application
        fields = ['file_path', 'description', 'is_private']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'zipfileform-description'}),
        }
