from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # password reset and password reset done view
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    # password reset and password reset done view
    path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),
    path('',views.dashboard,name='dashboard'),
]
