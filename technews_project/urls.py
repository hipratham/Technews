"""
URL configuration for technews_project project.
"""
from django.contrib import admin
from django.urls import path
from technews import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
