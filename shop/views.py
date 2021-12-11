from django.shortcuts import render
from .models import Good, Category, Company
from django.views.generic import ListView, DetailView
from shop_prj.crawler import get_detail, get_detail_img
from django.db.models import Q


# Create your views here.
class GoodList(ListView):
    model = Good
    ordering = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GoodList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['companies'] = Company.objects.all()
        return context



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
        context['sizes'] = self.object.size.all()
        context['colors'] = self.object.color.all()
        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        good_list = Good.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        good_list = Good.objects.filter(category=category)

    return render(request, 'shop/good_list.html',
                  {
                      'good_list' : good_list,
                      'categories' : Category.objects.all(),
                      'no_category_post_count' : Good.objects.filter(category=None).count(),
                      'category': category,
                  })


def mall_page(request, com_name):
    company = Company.objects.get(com_name=com_name)
    good_list = Good.objects.filter(company=company)

    return render(request, 'shop/good_list.html',
                  {
                      'good_list': good_list,
                      'categories': Category.objects.all(),
                      'company': company
                  })


def complex_page(request, company, slug):
    com_name = Company.objects.get(com_name=company)
    category = Category.objects.get(slug=slug)

    good_list = Good.objects.filter(Q(company=com_name)& Q(category=category))

    return render(request, 'shop/good_list.html',
                    {
                        'good_list': good_list,
                        'company': com_name,
                        'category': category
                    })


