from rest_framework import permissions
from .models import ShopMember, Product, Stock, Transaction, FinancialRecord


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        memberships = ShopMember.objects.filter(user=user)

        if memberships.filter(role="owner").exists():
            return True

        if memberships.filter(role="manager").exists():
            manager_shops = memberships.filter(role="manager").values_list("shop_id", flat=True)

            if isinstance(obj, Product):
                if obj.shop.id in manager_shops:
                    if request.method in permissions.SAFE_METHODS:
                        return True  
                    elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                        return True  
                return False


            if isinstance(obj, Stock):
                return obj.shop.id in manager_shops  

            if isinstance(obj, Transaction):
                return obj.shop.id in manager_shops 

            if isinstance(obj, FinancialRecord):
                if obj.shop.id in manager_shops:
                    return request.method in permissions.SAFE_METHODS 
                return False

            return False

        if memberships.filter(role="worker").exists():
            worker_shops = memberships.filter(role="worker").values_list("shop_id", flat=True)

            if isinstance(obj, Product):
                return obj.shop.id in worker_shops and request.method in permissions.SAFE_METHODS

            if isinstance(obj, Transaction):
                if obj.user == user:
                    return True
                if request.method == 'POST' and obj.shop.id in worker_shops:
                    return True
                return False

            if isinstance(obj, Stock):
                return obj.shop.id in worker_shops and request.method in permissions.SAFE_METHODS

            if isinstance(obj, FinancialRecord):
                return False  

            return False

        return False
