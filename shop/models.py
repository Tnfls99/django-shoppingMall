from django.db import models

# Create your models here.
# product
class Goods(models.Model):
    # 상품명
    name = models.TextField()
    # 간단한 설명
    about = models.CharField(max_length=500)
    # 상품 가격
    price = models.IntegerField()
    # 상품 이미지
    image = models.ImageField()
# company which makes product


