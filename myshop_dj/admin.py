from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile, Category
from django.contrib.auth.models import User


# Регистрация модели Категория
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Названия полей, отображаемых в списке
    search_fields = ('name',)  # Поля для поиска


# Регистрация модели Продукт
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')  # Названия полей
    list_filter = ('category',)  # Фильтры
    search_fields = ('name',)  # Поля для поиска


# Регистрация модели Корзина
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  # Названия полей
    search_fields = ('user__username',)  # Поля для поиска


# Регистрация модели Элемент Корзины
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  # Названия полей
    search_fields = ('cart__user__username', 'product__name')  # Поля для поиска


# Регистрация модели Заказ
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'created_at', 'address')  # Названия полей
    search_fields = ('user__username', 'full_name', 'email')  # Поля для поиска


# Регистрация модели Элемент Заказа
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')  # Названия полей
    search_fields = ('order__user__username', 'product__name')  # Поля для поиска


# Регистрация модели Профиль Пользователя
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email')  # Названия полей
    search_fields = ('user__username', 'email')  # Поля для поиска


# Регистрация всех моделей в админ-панели
admin.site.register(Category, CategoryAdmin)  # Регистрация категории
admin.site.register(Product, ProductAdmin)  # Регистрация продукта
admin.site.register(Cart, CartAdmin)  # Регистрация корзины
admin.site.register(CartItem, CartItemAdmin)  # Регистрация элемента корзины
admin.site.register(Order, OrderAdmin)  # Регистрация заказа
admin.site.register(OrderItem, OrderItemAdmin)  # Регистрация элемента заказа
admin.site.register(UserProfile, UserProfileAdmin)  # Регистрация профиля пользователя