from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home),
    path('login/', views.kakao_login),
    path('about_company/', views.about_com),
]