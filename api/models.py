from django.db import models
from accounts.models import CustomUser as User
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'


class Shop(models.Model):
    SHOP_TYPE_CHOICES = [
        ('online', 'Онлайн-магазин'),
        ('offline', 'Офлайн-магазин'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    shop_type = models.CharField(choices=SHOP_TYPE_CHOICES,default='offline',)
    address = models.TextField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Shop"
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"



class ShopMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Владелец'),
        ('manager', 'Менеджер'),
        ('worker', 'Сотрудник'),
    ]

    shop = models.ForeignKey(Shop, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="membership", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} – {self.get_role_display()}"

    class Meta:
        db_table = 'ShopMember'




class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField()
    barcode = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    size = models.CharField(null=True, blank=True)
    color = models.CharField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):

        if (not self.pk or not self.qr_code) and self.barcode:
            # Генерация QR-кода
            qr_img = qrcode.make(self.barcode)
        
            # Сохранение в буфер
            buffer = BytesIO()
            qr_img.save(buffer, 'PNG')

            # Сохранение в ImageField с уникальным именем файла
            filename = f'qr_code_{uuid.uuid4().hex}.png'
            self.qr_code.save(filename, File(buffer), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'


class Stock(models.Model):
    product = models.ForeignKey(Product, related_name='stocks', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='stocks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Stock'
        unique_together = ('product', 'shop')


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('in', 'Поступление'),
        ('out', 'Продажа'),
        ('adj', 'Корректировка'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, default='out')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    payment_method = models.ForeignKey("PaymentMethod", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Transaction'



class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Наличные'),
        ('CARD', 'Карта'),
        ('ONLINE', 'Онлайн'),
        ('OTHER', 'Другой'),
    ]

    name = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='payment_methods')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'PaymentMethod'
        unique_together = ('shop', 'name')
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"



class FinancialRecord(models.Model):
    FINANCIAL_TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=FINANCIAL_TYPE_CHOICES)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} ({self.category})"

    class Meta:
        db_table = 'FinancialRecord'





from django.db import models
from accounts.models import CustomUser as User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Notification'
        ordering = ['-created_at']
