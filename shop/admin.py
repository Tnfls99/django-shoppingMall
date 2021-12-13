from django.contrib import admin
from .models import Good, Company, Size, Color, Category, Tag, Comment

# Register your models here.
admin.site.register(Good)
admin.site.register(Company)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
