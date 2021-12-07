from django.db import models

# Create your models here.


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



    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

# company which makes product


