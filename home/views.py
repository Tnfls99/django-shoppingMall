from django.shortcuts import render, redirect
from shop.models import Good, Company, Category
from shop_prj.settings import KAKAO_REST_API_KEY
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    new_goods = Good.objects.order_by('-pk')[:3]
    return render(request, 'home/index.html', {'new_goods': new_goods})

def about_com(request):
    companies = Company.objects.all()
    categories = Category.objects.all()
    cnt = []
    for c in categories:
        products = Good.objects.filter(category=c)
        cnt.append(products.count())
    return render(request, 'home/about_company.html',
                  {
                      'companies': companies,
                      'cnt': cnt,
                  })

def kakao_login(request):
    app_rest_api_key = KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/accounts/kakao/login/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )