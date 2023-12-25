from django.shortcuts import render
from .models import Product,Brand,Review,ProductImage
from django.views.generic import ListView , DetailView


# Create your views here.



def mydebug(request):

    # Column Number -----------------
    # data = Product.objects.all()  #All
    # data = Product.objects.filter(price = 20)   
    # data = Product.objects.filter(price__gt = 98)  #Price Greater than 98
    # data = Product.objects.filter(price__gte = 98)  #Price greater than or equal 98
    # data = Product.objects.filter(price__lt = 98)  #Price less than  98
    # data = Product.objects.filter(price__lte = 98)  #Price less than or equal 98
    # data = Product.objects.filter(price__range = (80,83))  #Price Between 80 and 83


    # Relation -----------------
    # data = Product.objects.filter(brand__id = 5)
    # data = Product.objects.filter(brand__id__gt = 150)


    # Text ----------------------
    # data = Product.objects.filter(name__contains = 'Joseph')
    # data = Product.objects.filter(name__startswith = 'Joseph')
    data = Product.objects.filter(name__endswith = 'Joseph')

    return render (request,'products/debug.html',{'data':data})





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
    paginate_by = 50
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
    
    