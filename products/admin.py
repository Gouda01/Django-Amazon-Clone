from django.contrib import admin
from .models import Product , Brand , Review , ProductImage

# Register your models here.

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(ProductImage)