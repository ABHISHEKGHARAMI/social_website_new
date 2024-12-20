from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import CustomLogoutView


urlpatterns = [
    # path('login/',views.user_login,name='login'),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('logout_page/',views.logout_page,name='logout_page'),
    path('',views.dashboard,name='dashboard'),
]


