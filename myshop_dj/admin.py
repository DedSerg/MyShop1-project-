from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile, Category
from django.contrib.auth.models import User



# Регистрация модели Category в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Укажите, какие поля отображать в списке
    search_fields = ('name',)  # Позволяет искать по названию категории


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_product_name', 'full_name', 'email', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('full_name', 'email', 'user__username', 'product__name')
    ordering = ('-created_at',)

    def get_product_name(self, obj):
        return obj.product.name

    get_product_name.short_description = 'Название товара'
    get_product_name.admin_order_field = 'product__name'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email', 'date_of_birth')


# Регистрируем пользовательский класс администратора
admin.site.unregister(User)  # Убираем стандартный UserAdmin
admin.site.register(User)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
