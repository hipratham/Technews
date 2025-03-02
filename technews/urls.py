from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-news', views.generate_tech_news, name='generate-news'),
]
