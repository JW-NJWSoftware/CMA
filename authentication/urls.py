from django.contrib import admin
from django.urls import path
from authentication import views as auth_views

urlpatterns = [
    path('login/', auth_views.login_view, name="login_view"),
    path('logout/', auth_views.logout_view, name="logout_view"),
    path('register/', auth_views.register_view, name="register_view"),
    path('profile/', auth_views.profile_view, name="profile_view"),
    path('settings/', auth_views.settings_view, name="settings_view"),
]
