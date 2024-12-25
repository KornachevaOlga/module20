from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        return self.name



    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class CustomUser(AbstractUser):

    # Добавьте дополнительные поля, если необходимо
    email = models.EmailField(unique=True)  # Уникальный email
    # Пример дополнительного поля

    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Поле для номера телефона

    def __str__(self):
        return self.username
