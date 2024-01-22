from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import Brand,Product , ProductImage, Review


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductImage
        fields = ['image']

class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta :
        model = Review
        fields = ['user','review','rate','created_at']




class ProductListSerializer (TaggitSerializer, serializers.ModelSerializer):
    brand = serializers.StringRelatedField()   # To return brand name not id
    tags = TagListSerializerField()

    class Meta :
        model = Product
        #fields = '__all__'
        fields = ['name','price','flag','image','subtitle','description','sku','tags','brand','review_count','avg_rate']



class ProductDetailSerializer (TaggitSerializer, serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    images = ProductImagesSerializer(source='product_image',many=True) # To Show Product Images
    reviews = ProductReviewsSerializer(source='review_product',many=True) # To Show Product Reviews

    class Meta :
        model = Product
        #fields = '__all__'
        fields = ['name','price','flag','image','subtitle','description','sku','tags','brand','images','reviews','review_count','avg_rate']



class BrandListSerializer (serializers.ModelSerializer):
    class Meta :
        model = Brand
        fields = '__all__'

class BrandDetailSerializer (serializers.ModelSerializer):
    class Meta :
        model = Brand
        fields = '__all__'