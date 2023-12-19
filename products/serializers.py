from rest_framework import serializers
from .models import Brand,Product


class ProductListSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = '__all__'

class ProductDetailSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = '__all__'

class BrandListSerializer (serializers.ModelSerializer):
    class Meta :
        model = Brand
        fields = '__all__'

class BrandDetailSerializer (serializers.ModelSerializer):
    class Meta :
        model = Brand
        fields = '__all__'