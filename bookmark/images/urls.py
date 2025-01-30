from django.urls import path
from . import views

# app name
app_name = 'images'

urlpatterns = [
    path('create/',views.image_create,name='create'),
    path('detail/<int:id>/<slug:slug>/',
         views.image_detail,
         name='detail'),
    # url for the like or unlike the image
    path('like/',views.image_like,name='like'),
    path('',views.image_list,name='list'),
    path('ranking/', views.image_ranking, name='ranking'),
]
