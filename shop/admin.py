from django.contrib import admin
from .models import Good, Company, Size, Color

# Register your models here.
admin.site.register(Good)
admin.site.register(Company)
admin.site.register(Size)
admin.site.register(Color)
