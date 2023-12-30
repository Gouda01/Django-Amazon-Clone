from django.contrib import admin
from .models import Product , Brand , Review , ProductImage

# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin (admin.ModelAdmin):
   inlines = [ProductImagesInline]
   list_display = ['name','review_count','avg_rate']

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Review)
