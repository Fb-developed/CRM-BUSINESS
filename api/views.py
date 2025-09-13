from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

from .models import *
from .serializers import *

logger = logging.getLogger(__name__)

class SomeAPIView(APIView):
    def get(self, request):
        try:
            logger.debug("of SomeAPIView GET query")
            return Response({"message": "OK"})
        except Exception as e:
            logger.error(f"error  SomeAPIView.get: {e}")
            raise

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ShopMemberViewSet(viewsets.ModelViewSet):
    queryset = ShopMember.objects.all()
    serializer_class = ShopMemberSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer