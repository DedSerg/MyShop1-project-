from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Модель Категории
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)  # Поле для хранения изображений

    def __str__(self):
        return self.name

# Модель Корзины
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

# Модель Продукта
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def is_in_stock(self, quantity=1):
        return self.stock >= quantity

    def clean(self):
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        if self.stock < 0:
            raise ValidationError('Количество на складе не может быть отрицательным.')

# Модель Элемента Корзины
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='items', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError('Недостаточно товара на складе.')

    def increase_quantity(self):
        self.quantity += 1
        self.save()

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()

# Модель Заказа
class Order(models.Model):
    name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name} on {self.created_at}"

# Модель Элемента Заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')  # Укажите путь для загрузки изображений
    date_of_birth = models.DateField(null=True, blank=True)  # Поле для даты рождения
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Поле для телефона
    email = models.EmailField(max_length=254, null=True, blank=True)  # Поле для электронной почты
    last_name = models.CharField(max_length=150, null=True, blank=True)  # Поле для фамилии
    first_name = models.CharField(max_length=150, null=True, blank=True)  # Поле для имени

    def __str__(self):
        return f"{self.user.username}'s Profile"