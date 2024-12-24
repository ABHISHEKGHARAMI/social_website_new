from django import forms
from .models import Images


class ImageCreateForm(forms.Form):
    class Meta:
        model = Images
        fields = ['title','url','description']
        widgets = {
            'url':forms.HiddenInput
        }