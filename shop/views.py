from django.shortcuts import render
from .models import Good
from django.views.generic import ListView, DetailView
from shop_prj.crawler import get_detail, get_detail_img


# Create your views here.
class GoodList(ListView):
    model = Good
    ordering = 'pk'


class GoodDetail(DetailView):
    model = Good

    def get_context_data(self, **kwargs):
        url = self.object.from_url
        context = super(GoodDetail, self).get_context_data()
        detail = get_detail(url)
        if detail:
            context['detail'] = detail
        image = get_detail_img(url)
        context['img'] = image
        return context
