from django.urls import path, include
from . import views

urlpatterns = [
    path('create_good/', views.GoodCreate.as_view()),
    path('update_good/<int:pk>/', views.GoodUpdate.as_view()),
    path('delete/<int:pk>/', views.delete_good),
    path('category/<str:slug>', views.category_page),
    path('company/<str:com_name>', views.mall_page),
    path('search/<str:q>/', views.GoodSearch.as_view()),
    path('<str:company>/<str:slug>', views.complex_page),
    path('mypage/', views.mypage),
    path('<int:pk>/new_comment/', views.new_comment),
    path('malls/', views.all_malls),
    path('', views.GoodList.as_view()),
    path('<int:pk>/', views.GoodDetail.as_view()),
]
