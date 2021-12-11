from django.shortcuts import render, redirect
from shop.models import Good, Company
from shop_prj.settings import KAKAO_REST_API_KEY
import requests
from django.views.generic import View, FormView
from django.forms import forms
from shop.models import models
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    new_goods = Good.objects.order_by('-pk')[:6]
    return render(request, 'home/index.html', {'new_goods': new_goods})

def about_com(request):
    companies = Company.objects.all()
    return render(request, 'home/about_company.html', {'companies': companies})

def kakao_login(request):
    app_rest_api_key = KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/accounts/kakao/login/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )