from django.contrib import admin
from .models import Category, Product, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Регистрация модели Category в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Укажите, какие поля отображать в списке
    search_fields = ('name',)       # Позволяет искать по названию категории



# Register your models here.
class UserAdmin(BaseUserAdmin):
    actions = ['create_superuser']

    def create_superuser(self, request, queryset):
        for user in queryset:
            user.is_superuser = True
            user.is_staff = True
            user.save()
        self.message_user(request, _("Superuser created successfully."))

    create_superuser.short_description = "Администратор"

# Регистрируем пользовательский класс администратора
admin.site.unregister(User)  # Убираем стандартный UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(UserProfile)