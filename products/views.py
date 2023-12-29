from django.shortcuts import render
from django.db.models import Q , F
from django.db.models.aggregates import Count,Sum,Avg,Max,Min


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
    # data = Product.objects.filter(name__endswith = 'Joseph')
    # data = Product.objects.filter(price__isnull = True) #Price is null
    # data = Product.objects.filter(price__isnull = False) #Price is not null
    

    # Date ----------------------
    # data = Product.objects.filter(created_at__year = 2022) 
    # data = Product.objects.filter(created_at__month = 2) 
    # data = Product.objects.filter(created_at__day = 12) 
    

    # Complex Queries ----------------------
    # data = Product.objects.filter(flag = 'New',price__gt = 98) # 2 Conditions
    # data = Product.objects.filter(flag = 'New').filter(price__gt = 98) # same 2 Conditions

    # data = Product.objects.filter(
    #     Q(flag = 'New') &
    #     Q(price__gt = 98)
    #     ) # 2 Conditions  flag new AND price greater than 98

    # data = Product.objects.filter(
    #     Q(flag = 'New') |
    #     Q(price__gt = 98)
    #     )  # 2 Conditions  flag new OR price greater than 98
    
    # data = Product.objects.filter(
    #     ~ Q(flag = 'New') |
    #     Q(price__gt = 98)
    #     )  # 2 Conditions  flag not new OR price greater than 98
    

    # field reference ---------------------
    # data = Product.objects.filter(quantity = F('price')) # Quantity coulum = Price coulum
    # data = Product.objects.filter(quantity = F('brand__id')) # Quantity coulum = id coulum in Brand (Relation) 


    # Order ---------------------
    # data = Product.objects.order_by('name') # Order by name from a to z
    # data = Product.objects.order_by('-name') # Order by name from z to a
    # data = Product.objects.order_by('-name','price') # Order by name from z to a AND price fro big to little
    # data = Product.objects.order_by('name') [:10] # Order by name from a to z and show first 10
    # data = Product.objects.earliest('name') # Order by name from a to z and show first one
    # data = Product.objects.latest('name') # Order by name from a to z and show last one


    # Lmimit Fields ------------------
    # data = Product.objects.values('name','price') # To show all but get name and price coulums only
    # data = Product.objects.values_list('name','price') # To show all but get name and price coulums only
    # data = Product.objects.defer('subtitle') #To show all and get all coulums except subtitle


    # Lmimit related ------------------
    # data = Product.objects.select_related('brand').all() # One To One And One To Many Relation
    # data = Product.objects.select_related('brand').all() # Many To Many Relation
    # data = Product.objects.select_related('brand').select_related('category').all()


    # Aggregation : Count - Min - Max - Sum - AVG ------------------
    # data = Product.objects.aggregate(
    #     myavg = Avg('price'),
    #     mycount=Count('id'),
    #     mysum=Sum('price'),
    # )


    # Annotation :
    data = Product.objects.annotate(price_with_tax = F('price')*1.14)

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
    queryset = Brand.objects.annotate(product_count=Count('product_brand'))

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
        context["brand"] = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_brand'))[0]
        return context
    
    