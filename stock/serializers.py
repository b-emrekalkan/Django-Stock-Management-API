from itertools import product
from django.forms import ValidationError
from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name"
        )

class ProductSerializer(serializers.ModelSerializer):
    #! We use "stringRelated" to get the string equivalent of those connected with foreign key 👇

    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "stock"
        )
        #! 👇 "We added it as a read only field because we don't want the stock to be created in the post action.
        read_only_fields = ('stock',)

#? While on the Category page, we want to query the products of that category. For this, we need to write a serializer in a nested structure. 👇
class CategoryProductsSerializer(serializers.ModelSerializer):
    #! We used "many=True" because there can be more than one product belonging to the category. 👇
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "name",
            "products"
        )
class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            "id",
            "name",
            "phone",
            "address"
        )

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "user",
            "firm",
            "firm_id",
            "transaction",
            "product",
            "product_id",
            "quantity",
            "price",
            "price_total",
        )

        read_only_fields = ('price_total',)

    def validate(self, data):
        #! data, actually all of the above fields 👆
        if data.get('transaction') == 0:
            product = Product.objects.get(id=data.get('product_id'))
            if data.get('quantity') > product.stock:
                raise serializers.ValidationError(
                    f'Not enough stock! Current stock is {product.stock}'
                )
        return data