from rest_framework import serializers
from . import models as product_models


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    photo1 = serializers.SerializerMethodField()

    class Meta:
        model = product_models.Product
        fields = [
            "id",
            "user",
            "profile_photo",
            "title",
            "slug",
            "ref_code",
            "description",
            "price",
            "photo1",
            "views",
        ]

    def get_user(self, obj):
        return obj.user.full_name



class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = product_models.Product
        exclude = ["updated_at", "pkid"]


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.ProductViews
        exclude = ["updated_at", "pkid"]
        
        
# serializers.py

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    vendorName  = serializers.SerializerMethodField()
    discountPrice  = serializers.SerializerMethodField()
    vendorId  = serializers.SerializerMethodField()
    
    class Meta:
        model = product_models.Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'category','status','vendorName','rating','discountPrice','vendorId']
        
    def get_id(self,obj):
        return obj.pk
        
    def get_name(self,obj):
        return obj.title
    
    def get_discountPrice(self,obj):
        return obj.discount_price
    
    def get_vendorName(self,obj):
        if obj.user:
            return obj.user.full_name
        return ' '
    
    def get_vendorId(self,obj):
        if obj.user:
            return obj.user.pk
        return ' '
    
    def get_category(self,obj):
        if obj.category:
            return obj.category.name
        return ""
    
    def get_stock(self,obj):
        return obj.stock_quantity
    
    def get_image(self,obj):
        return obj.photo1
    
    def get_status(self,obj):
        return "Active"
