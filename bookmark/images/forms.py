from django import forms
from .models import Image
from django.utils.text import slugify
import requests
from django.core.files.base import ContentFile


class ImageCreateForm(forms.Form):
    class Meta:
        model = Image
        fields = ['title','url','description']
        widgets = {
            'url':forms.HiddenInput
        }
    
    # cleaning and checking the url
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg','png']
        extensions = url.rsplit('.',1)[1].lower()
        if extensions not in valid_extensions:
            raise forms.ValidationError('Image not supported!!')
        return url
    
    # have to save the image in the database when it fetch the image using the requests
    def save(self,force_insert=False,force_update=False,commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.',1)[1].lower()
        image_name = f"{name}.{extension}"
        # download the image using the request
        response = requests.get(image_url)
        #save the image
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )
        
        if commit:
            image.save()
        return image
        
        