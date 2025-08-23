from rest_framework import serializers
from .models import Product, Shop, Category, ShopMember, Stock, Transaction, PaymentMethod, FinancialRecord


class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.CharField(source='shop.name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    stock_quantity = serializers.IntegerField(source='stock.quantity', read_only=True)
    qr_code_url = serializers.SerializerMethodField() 

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_at", "barcode", "shop", "category", "stock_quantity", "qr_code_url")

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code and hasattr(obj.qr_code, 'url'):
            return request.build_absolute_uri(obj.qr_code.url) if request else obj.qr_code.url
        return None





class ShopSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"
        read_only_fields = ("created_at", "user",)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('created_at',)



class ShopMemberSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    shop = serializers.CharField(source='shop.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = ShopMember
        fields = "__all__"
        read_only_fields = ('user', 'shop', 'role_display', "created_at",)



class StockSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    shop = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = Stock
        fields = "__all__"
        read_only_fields = ('created_at', 'product', 'shop',)



class TransactionSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    shop = serializers.CharField(source='shop.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    payment_method = serializers.CharField(source='payment_method.name', read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ('id', 'product', 'shop', 'user', 'payment_method', 'created_at',)



class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"




class FinancialRecordSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    shop = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = FinancialRecord
        fields = "__all__"
        read_only_fields = ('id', 'user', 'shop', 'created_at',)
