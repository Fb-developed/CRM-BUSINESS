from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'shops', ShopViewSet)
router.register(r'shop-members', ShopMemberViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'financial-records', FinancialRecordViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = router.urls
