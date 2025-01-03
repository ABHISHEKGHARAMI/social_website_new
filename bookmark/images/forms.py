#  creating the form for the user to fetch the image
from django import forms
from .models import Image
import requests
from django.utils.text import slugify
from django.core.files.base import ContentFile


# the form
class ImageCreateForm(forms.Form):
    class Meta:
        model = Image
        fields = ['title','url','description']
        widget = {
            'url':forms.HiddenInput
        }
        
    # checking the url is valid or not
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpeg','jpg','png']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The url given does not match with the extensions'
            )
        return url
    
    
    # override the save method for the images 
    def save(self,force_insert=False,force_update=False,commit=False):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.',1)[1].lower()
        image_name = f'{name}.{extension}'
        # download the image from the internet
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )
        # finally commit the image
        if commit:
            image.save()
        return image
        
    
    