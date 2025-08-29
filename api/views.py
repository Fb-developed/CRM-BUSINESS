# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.shortcuts import get_object_or_404
# from .models import Product, Shop, Transaction, Notification
# from .serializers import ProductSerializer, ShopSerializer, TransactionSerializer, NotificationSerializer
# from .permissions import RolePermission


# class ProductListCreate(APIView):
#     permission_classes = [IsAuthenticated, RolePermission]

#     def get(self, request):

#         if request.user.is_superuser:
#             products = Product.objects.all()
#         else:
#             products = []
#             for product in Product.objects.all():
#                 try:
#                     self.check_object_permissions(request, product)
#                     products.append(product)
#                 except:
#                     pass
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         # Создать новый продукт.
#         # Проверяем, что пользователь имеет права на создание продукта в магазине.
#         serializer = ProductSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             product = serializer.save()
#             try:
#                 self.check_object_permissions(request, product)
#             except:
#                 product.delete()  # Удаляем, если нет прав
#                 return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductDetail(APIView):
#     permission_classes = [IsAuthenticated, RolePermission]

#     def get_object(self, pk, request):

        
#         product = get_object_or_404(Product, pk=pk)
#         self.check_object_permissions(request, product)
#         return product

#     def get(self, request, pk):
#         product = self.get_object(pk, request)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         product = self.get_object(pk, request)
#         serializer = ProductSerializer(product, data=request.data, partial=False, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         product = self.get_object(pk, request)
#         serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         product = self.get_object(pk, request)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ShopListCreate(APIView):
#     permission_classes = [IsAuthenticated, RolePermission]

#     def get(self, request):
#         shops = []
#         for shop in Shop.objects.all():
#             try:
#                 self.check_object_permissions(request, shop)
#                 shops.append(shop)
#             except:
#                 pass
#         serializer = ShopSerializer(shops, many=True)
#         return Response(serializer.data)

#     def post(self, request):

#         serializer = ShopSerializer(data=request.data)
#         if serializer.is_valid():
#             shop = serializer.save(user=request.user)
#             self.check_object_permissions(request, shop)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TransactionListCreate(APIView):
#     permission_classes = [IsAuthenticated, RolePermission]

#     def get(self, request):
#         """
#         Получить список транзакций, доступных пользователю.
#         """
#         transactions = []
#         for transaction in Transaction.objects.all():
#             try:
#                 self.check_object_permissions(request, transaction)
#                 transactions.append(transaction)
#             except:
#                 pass
#         serializer = TransactionSerializer(transactions, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         """
#         Создать новую транзакцию (продажу).
#         """
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             transaction = serializer.save(user=request.user)
#             try:
#                 self.check_object_permissions(request, transaction)
#             except:
#                 transaction.delete()
#                 return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class NotificationViewSet(viewsets.ModelViewSet):
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny # Импорти нави AllowAny
from django.shortcuts import get_object_or_404
from .models import Product, Shop, Transaction, Notification
from .serializers import ProductSerializer, ShopSerializer, TransactionSerializer, NotificationSerializer
from rest_framework import viewsets


# Инҷо мо IsAuthenticated ва RolePermission-ро бо AllowAny иваз кардем.
# Ин маънои онро дорад, ки ҳар як истифодабаранда метавонад ба ин view дастрасӣ дошта бошад.

class ProductListCreate(APIView):
    permission_classes = [AllowAny] # Иҷозатҳои оммавӣ

    def get(self, request):
        # Ҳамаи маҳсулотро дастрас кардан (бе филтр)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Эҷоди маҳсулоти нав (дастрас барои ҳама)
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    permission_classes = [AllowAny] # Иҷозатҳои оммавӣ

    def get_object(self, pk, request):
        product = get_object_or_404(Product, pk=pk)
        return product

    def get(self, request, pk):
        product = self.get_object(pk, request)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk, request)
        serializer = ProductSerializer(product, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk, request)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk, request)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopListCreate(APIView):
    permission_classes = [AllowAny] # Иҷозатҳои оммавӣ

    def get(self, request):
        # Ҳамаи мағозаҳоро дастрас кардан (бе филтр)
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Эҷоди мағозаи нав (дастрас барои ҳама)
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListCreate(APIView):
    permission_classes = [AllowAny] # Иҷозатҳои оммавӣ

    def get(self, request):
        # Ҳамаи транзаксияҳоро дастрас кардан (бе филтр)
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Эҷоди транзаксияи нав (дастрас барои ҳама)
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] # Иҷозатҳои оммавӣ
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Ин қисм бояд тағир дода шавад, зеро Notification.objects.filter(user=self.request.user)
        # ба корбари воридшуда ниёз дорад. Агар AllowAny бошад, self.request.user метавонад AnonymousUser бошад.
        # Агар шумо хоҳед, ки ҳамаи notifications-ро нишон диҳед, queryset-ро ба ин тағйир диҳед:
        return Notification.objects.all()