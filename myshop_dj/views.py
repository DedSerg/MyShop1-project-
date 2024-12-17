from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Category, Product, Cart, CartItem, Order, UserProfile
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, OrderForm, UserProfileForm
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F


def home(request):
    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'myshop_dj/home.html', {'categories': categories})

class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Получаем категорию по ID
    products = Product.objects.filter(category=category).all()
    if not products.exists():
        print("Продукты не найдены для этой категории.")  # Вывод в консоль для отладки

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')  # Получаем номер страницы из параметров запроса
    page_obj = paginator.get_page(page_number)

    return render(request, 'myshop_dj/category_detail.html', {
        'category': category,
        'page_obj': page_obj,
    })

def category_list(request):
    categories = Category.objects.all()  # Извлечение всех категорий из базы данных
    return render(request, 'myshop_dj/category_list.html', {'categories': categories})

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def product_list(request):
    product_list = Product.objects.all()  # Получаем все продукты
    paginator = Paginator(product_list, 6)  # Показывать 6 продуктов на странице
    page_number = request.GET.get('page')  # Получаем номер страницы
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    return render(request, 'myshop_dj/product_list.html', {
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Получаем продукт по первичному ключу
    return render(request, 'myshop_dj/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)  # Получаем или создаем корзину
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = float(quantity)
        except ValueError:
            quantity = 1  # Установить по умолчанию
        if not created:   # Если товар уже в корзине, увеличиваем количество на введенное значение
            cart_item.quantity += quantity
        else:    # Если товар только что добавлен, устанавливаем количество на введенное значение
            cart_item.quantity = quantity
        cart_item.save()  # Сохраняем изменения

    return redirect('cart_view')  # Перенаправляем на страницу корзины

def cart_view(request):
    if request.user.is_authenticated:
        # Получаем или создаем корзину текущего пользователя
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Получаем все элементы корзины для текущей корзины
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')  # Оптимизация запросов
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return render(request, 'myshop_dj/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)  # Установить значение по умолчанию
        try:
            quantity = int(quantity)  # Преобразуем в целое число
        except ValueError:
            quantity = 1  # Установить по умолчанию, если не удалось преобразовать

        # Получаем корзину текущего пользователя
        cart = get_object_or_404(Cart, user=request.user)

        # Попробуем получить CartItem, связанный с продуктом и корзиной
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if cart_item:  # Если CartItem найден
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество товара обновлено.')  # Сообщение об успешном обновлении
        else:
            messages.error(request, 'Товар не найден в вашей корзине.')  # Сообщение об ошибке

    return redirect('cart_view')  # Перенаправление на страницу корзины

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)# Получаем CartItem по его ID
    if request.user.is_authenticated:
        if cart_item.cart.user == request.user:# Проверяем, принадлежит ли товар текущему пользователю
           cart_item.delete()  # Удаляем товар из корзины
           messages.success(request, 'Товар успешно удален из корзины.')  # Сообщение об успешном удалении
        else:
            messages.error(request, 'Вы не можете удалить этот товар из корзины.')  # Если товар не принадлежит пользователю
    else:
        messages.error(request, 'Пожалуйста, войдите в систему, чтобы удалить товар из корзины.')

    return redirect('cart_view')  # Перенаправляем обратно на страницу корзины


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            login(request, user)  # Автоматически входим в систему после регистрации

            # Приветственное сообщение
            messages.success(request, f'Добро пожаловать, {user.first_name} {user.last_name}!')
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = UserRegistrationForm()  # Создаем пустую форму, если это GET-запрос

    # Рендерим страницу регистрации с формой
    return render(request, 'myshop_dj/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Входим в систему
                messages.success(request, f'Добро пожаловать, {username}!')  # Приветственное сообщение
                return redirect('home')  # Перенаправление на главную страницу после входа
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'myshop_dj/login.html', {'form': form})  # Указываем путь к шаблону логина

class CustomLoginView(LoginView):
    template_name = 'myshop_dj/login.html'
    success_url = reverse_lazy('profile')  # Укажите имя URL для перенаправления


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'myshop_dj/profile.html'  # Укажите ваш шаблон для профиля

def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)  # Получение или создание профиля

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Обработка формы
        if form.is_valid():
            form.save()  # Сохранение формы
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserProfileForm(instance=user_profile)  # Заполнение формы существующими данными

    return render(request, 'myshop_dj/profile.html', {'user': request.user, 'user_profile': user_profile, 'form': form})

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user'] = self.request.user  # Добавляем текущего пользователя в контекст
    return context


def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()  # Сохраняем заказ
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('category_list')  # Перенаправление на страницу покупок
    else:
        form = OrderForm()

    return render(request, 'myshop_dj/checkout.html', {'form': form})


@require_POST  # Ограничение на прием только POST-запросов
def process_order(request):
    form = OrderForm(request.POST)

    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user  # Привязка заказа к текущему пользователю
        order.save()

        # Редирект на страницу завершения заказа, передавая order.id
        return redirect('order_complete', order_id=order.id)  # Передаем order.id

    # Если форма не валидна, возвращаем её на страницу с ошибками
    return render(request, 'myshop_dj/checkout.html', {'form': form})


def order_complete(request, order_id):
    # Получаем заказ по ID или возвращаем 404, если не найден
    order = get_object_or_404(Order, id=order_id)

    # Вычисляем общую стоимость на основе quantity и product.price
    total_price = order.items.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or 0  # Используем 0, если нет элементов

    # Формируем контекст для передачи в шаблон
    context = {
        'order': order,
        'total_price': total_price,
    }

    return render(request, 'myshop_dj/order_complete.html', context)