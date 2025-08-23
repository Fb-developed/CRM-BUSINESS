from rest_framework import permissions
from .models import ShopMember


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        u = request.user
        mems = ShopMember.objects.filter(user=u)

        # owner
        if mems.filter(role="owner").exists():
            return True

        # manager
        if mems.filter(role="manager").exists():
            shops = mems.filter(role="manager").values_list("shop_id", flat=True)
            if hasattr(obj, "shop"):
                return obj.shop.id in shops
            if hasattr(obj, "product"):
                return obj.product.shop.id in shops
            return False

        # worker
        if mems.filter(role="worker").exists():
            if hasattr(obj, "user"):
                return obj.user == u
            return False

        return False
