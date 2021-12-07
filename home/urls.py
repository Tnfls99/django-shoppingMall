from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about_company/', views.about_com),
]