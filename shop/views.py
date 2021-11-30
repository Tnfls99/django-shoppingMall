from django.shortcuts import render
from .models import Good

# Create your views here.
def index(request):
    goods = Good.objects.all().order_by('pk')

    return render(
        request,
        'shop/good_list.html',
        {
            'goods' : goods
        }
    )
