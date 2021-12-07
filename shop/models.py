from django.db import models

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


class Color(models.Model):

    color = models.CharField(max_length=50)

    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.company}] - {self.color}'


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
    about = models.TextField()
    # 상품 가격
    price = models.IntegerField()
    # 재고
    inventory = models.IntegerField(blank=False)
    # 상품 이미지
    image = models.ImageField(upload_to='shop/images/', blank=False)
    # 상품 상세페이지를 위한 자사몰 url
    from_url = models.URLField()
    # 일대다 관계 (상품 - 회사)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    # 상품 사이즈
    size = models.ManyToManyField(Size)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

