from django.shortcuts import render, redirect
from .models import Good, Category, Company, Tag, Comment
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from shop_prj.crawler import get_detail, get_detail_img
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from . import form

# Create your views here.


def delete_good(request, pk):
    good = Good.objects.get(pk=pk)
    good.delete()
    return redirect('/shop/')


class GoodCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Good

    fields = ['name', 'about', 'price', 'image', 'inventory', 'from_url', 'company', 'size', 'color', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        # 로그인이 되어져 있으면서 스태프 인가
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.user_com = current_user
            response = super(GoodCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str') # template의 input name과 일치해야한다.
            if tags_str:
                tags_str = tags_str.strip() # 공백제거
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t) # 태그 모델을 받아옴
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True) # 한글에 대한 태그 허용
                        tag.save()
                    self.object.tag.add(tag)
            return response
        else:
            return redirect('/shop/')


class GoodUpdate(LoginRequiredMixin, UpdateView): # 모델명_form 템플릿명으로 사용
    model = Good
    fields = ['name', 'about', 'price', 'image', 'inventory', 'from_url', 'company', 'size', 'color', 'category']

    # update인 경우 별도의 이름 지정 필요
    template_name = 'shop/good_update_form.html'

    def dispatch(self, request, *args, **kwargs): # Get으로 접근했는지 Post로 접근했는지 구분해주는 함수 - 장고가 제공
        if request.user.is_authenticated and request.user == self.get_object().user_com:
            return super(GoodUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GoodUpdate, self).get_context_data()
        if self.object.tag.exists():
            tags_str_list = list()
            for t in self.object.tag.all():
                tags_str_list.append(t.name)
            context['tag_str_default'] = '; '.join(tags_str_list)
        return context

    def form_valid(self, form):
        # 다시 user에 대한 권한 체크를 할 필요가 없다.
        response = super(GoodUpdate, self).form_valid(form)
        # 기존에 있던 태그 지우기
        self.object.tag.clear() # 태그가 다시 만들어진다
        tags_str = self.request.POST.get('tags_str')  # template의 input name과 일치해야한다.
        if tags_str:
            tags_str = tags_str.strip()  # 공백제거
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 태그 모델을 받아옴
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)  # 한글에 대한 태그 허용
                    tag.save()
                self.object.tag.add(tag)
        return response


class GoodList(ListView):
    model = Good
    ordering = 'pk'
    paginate_by = 12

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
        context['comment_form'] = CommentForm
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


def all_malls(request):
    companies = Company.objects.all()
    goods = []
    for com in companies:
        g = Good.objects.filter(company=com)
        if len(g) > 3:
            goods.append(g[:3])
        else:
            goods.append(g)


    return render(request, 'shop/goods_by_malls.html',
                  {
                      'goods': goods,
                  })
