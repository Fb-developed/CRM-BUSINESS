from django.db import models
from accounts.models import CustomUser as User


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'



class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Shop'



class ShopMember(models.Model):
    shop = models.ForeignKey(Shop, related_name="shop_member", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_member", on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    can_veiw = models.BooleanField()
    can_edit = models.BooleanField()
    can_manage_stock = models.BooleanField()

    def __str__(self):
        return self.role

    class Meta:
        db_table = 'Shop_member'
        unique_together = (('shop', 'user'),)



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'




class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    created_at = models.DateField()

    class Meta:
        db_table = 'Stock'
        unique_together = (('product', 'shop'),)



class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    type = models.CharField(max_length=255)
    seling_price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()

    class Meta:
        db_table = 'Transaction'
        unique_together = (('product', 'shop', 'user'),)



class FinancialRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    type = models.CharField(max_length=255)
    created_at = models.DateField()

    class Meta:
        db_table = 'FinancialRecord'
        unique_together = (('user', 'shop'),)




class Supplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    address = models.TextField()
    notes = models.TextField()
    created_at = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Supplier'



class Purchase(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField()
    notes = models.TextField()
    created_at = models.DateField()

    class Meta:
        db_table = 'Purchase'
        unique_together = (('shop', 'supplier', 'user'),)



class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    cost_pric = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'PurchaseItem'
        unique_together = (('purchase', 'product'),)