#  creating the form for the user to fetch the image
from django import forms
from .models import Image


# the form
class ImageForm(forms.Form):
    class Meta:
        model = Image
        fields = ['title','url','description']
        widget = {
            'url':forms.HiddenInput
        }
    
    