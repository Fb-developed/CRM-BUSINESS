from django.contrib import admin
from .models import Category, Shop, Product, ShopMember, Stock, Transaction, PaymentMethod, FinancialRecord

admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ShopMember)
admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(PaymentMethod)
admin.site.register(FinancialRecord)
