from django.urls import path
from .views import ProductListCreate, ProductDetail, ShopListCreate, TransactionListCreate

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('shops/', ShopListCreate.as_view(), name='shop-list-create'),
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
]


