from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product, Shop, Transaction
from .serializers import ProductSerializer, ShopSerializer, TransactionSerializer
from .permissions import RolePermission


class ProductListCreate(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def get(self, request):
        products = Product.objects.all()
        if not request.user.is_superuser:
            products = [p for p in products if self.check_object_permissions(request, p) is None]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            if not self.check_object_permissions(request, product) is None:
                return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def get_object(self, request, pk):
        try:
            obj = Product.objects.get(pk=pk)
            self.check_object_permissions(request, obj)
            return obj
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(request, pk)
        if not product:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(request, pk)
        if not product:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            self.check_object_permissions(request, updated)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(request, pk)
        if not product:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


class ShopListCreate(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def get(self, request):
        shops = Shop.objects.all()
        shops = [s for s in shops if self.check_object_permissions(request, s) is None]
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save(user=request.user)
            self.check_object_permissions(request, shop)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListCreate(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    def get(self, request):
        transactions = Transaction.objects.all()
        transactions = [t for t in transactions if self.check_object_permissions(request, t) is None]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=request.user)
            self.check_object_permissions(request, transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
