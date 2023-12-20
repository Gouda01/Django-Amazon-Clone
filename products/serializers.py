from rest_framework import serializers
from .models import Brand,Product


class ProductListSerializer (serializers.ModelSerializer):
    brand = serializers.StringRelatedField()   # To return brand name not id
    review_count = serializers.SerializerMethodField() # To Show Review count
    avg_rate = serializers.SerializerMethodField() # To Show Review Average
    class Meta :
        model = Product
        fields = '__all__'


    # To Show Review count
    def get_review_count(self,object): 
        reviews = object.review_product.all().count()
        return reviews

    # To Show Review Average
    def get_avg_rate(self,object): 
        reviews = object.review_product.all()
        total = 0

        for item in reviews :
            total += item.rate
        if len(reviews) > 0 :
            avg = total / len(reviews)
        else:
            avg = 0
        return avg



class ProductDetailSerializer (serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    review_count = serializers.SerializerMethodField() # To Show Review count
    avg_rate = serializers.SerializerMethodField() # To Show Review Average
    class Meta :
        model = Product
        fields = '__all__'

    # To Show Review Average
    def get_avg_rate(self,object): 
        reviews = object.review_product.all()
        total = 0

        for item in reviews :
            total += item.rate
        if len(reviews) > 0 :
            avg = total / len(reviews)
        else:
            avg = 0
        return avg



    # To Show Review count
    def get_review_count(self,object): 
        reviews = object.review_product.all().count()
        return reviews
    


class BrandListSerializer (serializers.ModelSerializer):
    class Meta :
        model = Brand
        fields = '__all__'

class BrandDetailSerializer (serializers.ModelSerializer):
    class Meta :
        model = Brand
        fields = '__all__'