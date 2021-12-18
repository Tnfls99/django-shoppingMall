from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.


# company which makes product
class Company(models.Model):
    # 회사명
    com_name = models.CharField(max_length=30)
    #  회사 주소
    address = models.TextField()
    # 회사 연락처
    contact = models.CharField(max_length=100)
    # 회사 자사몰 링크
    com_url = models.URLField()
    # 회사 계좌번호
    bank_account = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.com_name}'

    def get_absolute_url(self):
        return f'/shop/company/{self.com_name}'

    def get_complex_url(self):
        return f'/shop/{self.com_name}'


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}'


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/shop/tags/{self.name}'


# product options
class Color(models.Model):

    color = models.CharField(max_length=50)

    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.company}] - {self.color}'

    def get_color(self):
        return f'{self.color}'


class Size(models.Model):
    # 사이즈 종류를 위한 필드
    version = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.version}'


# product
class Good(models.Model):
    # 상품명
    name = models.TextField()
    # 간단한 설명
    about = MarkdownxField()
    # 상품 가격
    price = models.IntegerField()
    # 재고
    inventory = models.IntegerField(blank=False)
    # 상품 이미지
    image = models.ImageField(upload_to='shop/images/', blank=False)
    # 상품 상세페이지를 위한 자사몰 url
    from_url = models.URLField()
    # 일대다 관계 (상품 - 회사)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    # 상품 사이즈
    size = models.ManyToManyField(Size)
    # 상품 색상
    color = models.ManyToManyField(Color)
    # 카테고리
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    # 태그
    tag = models.ManyToManyField(Tag)
    # 상품 등록한 사람
    user_com = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.about)


class Comment(models.Model): # 블로그 포스트가 존재해야만 댓글을 달 수 있다. 댓글과 포스트는 다대일 관계
    good = models.ForeignKey(Good, on_delete=models.CASCADE) # 포스트가 삭제되면 댓글도 모두 삭제
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 한명의 유저가 여러개의 댓글을 달 수 있기 때문에 다대일 관계
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}::{self.content}'

    def get_absolute_url(self):
        return f'{self.good.get_absolute_url()}#comment-{self.pk}'


