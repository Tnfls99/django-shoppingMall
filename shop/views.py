from django.shortcuts import render, redirect
from .models import Good, Category, Company, Tag, Comment
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from shop_prj.crawler import get_detail, get_detail_img
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404

# Create your views here.


class GoodList(ListView):
    model = Good
    ordering = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GoodList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['companies'] = Company.objects.all()
        return context


class GoodSearch(GoodList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']  # 검색어 가지고 옴
        post_list = Good.objects.filter(
            Q(name__contains=q) | Q(category__name__contains=q) | Q(company__com_name__contains=q) # 데이터베이스에서 쿼리를 통해 데이터를 찾아옴
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(GoodSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'{q}에 대한 검색 결과 ({self.get_queryset().count()})'

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
        comments = Comment.objects.filter(good=self.object)


        context['comments'] = comments
        context['img'] = image
        context['sizes'] = self.object.size.all()
        context['colors'] = self.object.color.all()
        context['tags'] = self.object.tag.all()
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
                      'companies': Company.objects.all(),
                  })


def mall_page(request, com_name):
    company = Company.objects.get(com_name=com_name)
    good_list = Good.objects.filter(company=company)

    return render(request, 'shop/good_list.html',
                  {
                      'good_list': good_list,
                      'categories': Category.objects.all(),
                      'company': company,
                      'companies': Company.objects.all()
                  })


def complex_page(request, company, slug):
    com_name = Company.objects.get(com_name=company)
    category = Category.objects.get(slug=slug)

    good_list = Good.objects.filter(Q(company=com_name)& Q(category=category))

    return render(request, 'shop/good_list.html',
                    {
                        'good_list': good_list,
                        'company': com_name,
                        'category': category,
                        'categories': Category.objects.all(),
                    })


def tags_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    good_list = Good.objects.get(tag=tag)

    return render(request, 'shop/good_list.html',
                  {
                      'good_list': good_list,
                      'tag': tag
                  })


def mypage(request):
    user = request.user
    name = user.username
    if user.socialaccount_set.exists():
        avatar = user.socialaccount_set.first().get_avatar_url()
    else:
        avatar = 'https://doitdjango.com/avatar/id/426/215f50b97258a737/svg/{user.email}/'

    if user.email:
        email = user.email
    else:
        email = False

    return render(request, 'shop/mypage.html',
                  {
                        'username' : name,
                        'avatar' : avatar,
                        'email': email,
                        'comments': Comment.objects.filter(user=user),
                  })


def new_comment(request, pk):
    if request.user.is_authenticated:
        good = get_object_or_404(Good, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.good = good
                comment.user = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(good.get_absolute_url())
        else:
            raise PermissionDenied
