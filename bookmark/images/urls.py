from django.urls import path
from . import views


app_name = 'images'


# urlpatterns for the user
urlpatterns = [
    path('create/',views.image_create,name='image_create'),
]
