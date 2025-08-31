from unfold.admin import ModelAdmin
from .models import *
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    def has_module_permission(self, request):
        return True

@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = ("name", "shop_type", "address", "user", "created_at")
    list_filter = ("shop_type",)
    search_fields = ("name", "address")
    def has_module_permission(self, request):
        return True

@admin.register(ShopMember)
class ShopMemberAdmin(ModelAdmin):
    list_display = ("shop", "user", "role")
    list_filter = ("role",)
    search_fields = ("user__username",)
    def has_module_permission(self, request):
        return True

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "price", "shop", "barcode", "category", "created_at")
    list_filter = ("category", "shop")
    search_fields = ("name", "barcode")
    def has_module_permission(self, request):
        return True

@admin.register(Stock)
class StockAdmin(ModelAdmin):
    list_display = ("product", "shop", "quantity", "created_at")
    list_filter = ("shop",)
    search_fields = ("product__name",)
    def has_module_permission(self, request):
        return True

@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ("product", "quantity", "type", "selling_price", "user", "created_at")
    list_filter = ("type", "payment_method")
    search_fields = ("product__name",)
    def has_module_permission(self, request):
        return True

@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ("name", "shop")
    list_filter = ("shop",)
    search_fields = ("name",)
    def has_module_permission(self, request):
        return True

@admin.register(FinancialRecord)
class FinancialRecordAdmin(ModelAdmin):
    list_display = ("type", "amount", "category", "shop", "user", "created_at")
    list_filter = ("type", "shop")
    search_fields = ("category",)
    def has_module_permission(self, request):
        return True

@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("user", "message", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("message",)
    def has_module_permission(self, request):
        return True
