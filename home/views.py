from django.shortcuts import render
from shop.models import Good


# Create your views here.
def home(request):
    new_goods = Good.objects.order_by('-pk')[:6]
    return render(request, 'home/index.html', {'new_goods': new_goods})