from django.shortcuts import render
from .models import Product,Brand,Review,ProductImage
from django.views.generic import ListView , DetailView


# Create your views here.

class ProductList (ListView) :
    model = Product
    paginate_by = 50


class ProductDetail (DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product = self.get_object())
        context["images"] = ProductImage.objects.filter(product = self.get_object())
        context["related"] = Product.objects.filter(brand = self.get_object().brand)
        return context


class BrandList (ListView) :
    model = Brand
    paginate_by = 50

class BrandDetail (ListView):
    model = Product
    template_name = 'products/brand_detail.html'

    # Return Products of the brand
    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset = super().get_queryset().filter(brand=brand)
        return queryset
    
    # Return Brand Details
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(slug=self.kwargs['slug'])
        return context
    
    