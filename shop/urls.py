from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.GoodList.as_view()),
    path('<int:pk>/', views.GoodDetail.as_view()),
]
