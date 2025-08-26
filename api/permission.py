from rest_framework import permissions
from .models import ShopMember, Product, Stock, Transaction, FinancialRecord


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверка: пользователь должен быть аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        memberships = ShopMember.objects.filter(user=user)

        # Владелец имеет полный доступ
        if memberships.filter(role="owner").exists():
            return True

        # Менеджер
        if memberships.filter(role="manager").exists():
            manager_shops = memberships.filter(role="manager").values_list("shop_id", flat=True)

            # Товар 
            if isinstance(obj, Product):
                if obj.shop.id in manager_shops:
                    if request.method in permissions.SAFE_METHODS:
                        return True  # может просматривать
                    elif request.method in ['POST', 'PUT', 'PATCH']:
                        return True  # может редактировать / создавать
                    elif request.method == 'DELETE':
                        return False  # не может удалять товары
                return False

            #  Остатки 
            if isinstance(obj, Stock):
                return obj.shop.id in manager_shops  # просмотр и редактирование

            #  Транзакции 
            if isinstance(obj, Transaction):
                return obj.shop.id in manager_shops  # просмотр и создание

            #  Финансы 
            if isinstance(obj, FinancialRecord):
                if obj.shop.id in manager_shops:
                    return request.method in permissions.SAFE_METHODS  # только чтение
                return False

            return False

        # Работник
        if memberships.filter(role="worker").exists():
            worker_shops = memberships.filter(role="worker").values_list("shop_id", flat=True)

            # --- Товары ---
            if isinstance(obj, Product):
                return obj.shop.id in worker_shops and request.method in permissions.SAFE_METHODS

            # --- Транзакции ---
            if isinstance(obj, Transaction):
                # Может просматривать свои продажи
                if obj.user == user:
                    return True
                # Может создавать продажи
                if request.method == 'POST' and obj.shop.id in worker_shops:
                    return True
                return False

            # --- Остатки ---
            if isinstance(obj, Stock):
                return obj.shop.id in worker_shops and request.method in permissions.SAFE_METHODS

            # --- Финансовые записи ---
            if isinstance(obj, FinancialRecord):
                return False  # сотрудникам запрещён доступ

            return False

        # Нет роли — нет доступа
        return False
