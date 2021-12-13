from django.urls import path, include
from . import views

urlpatterns = [
    path('category/<str:slug>', views.category_page),
    path('company/<str:com_name>', views.mall_page),
    path('<str:company>/<str:slug>', views.complex_page),
    path('mypage/', views.mypage),
    path('<int:pk>/new_comment/', views.new_comment),
    path('', views.GoodList.as_view()),
    path('<int:pk>/', views.GoodDetail.as_view()),
]
