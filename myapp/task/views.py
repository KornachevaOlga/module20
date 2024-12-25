from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserRegistrationForm, CustomUserLoginForm
from django.contrib import messages  # Импортируем систему сообщений

# Create your views here.

def platform(request):
    return render(request, 'platform.html', context={'username': request.user.username})  # Шаблон первой страницы

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products, 'username': request.user.username})

def product_detail(request, item_id):
    product = get_object_or_404(Product, id=item_id)  # Получаем товар по ID
    return render(request, 'product_detail.html', {'product': product, 'username': request.user.username})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход после регистрации
            messages.success(request, f'Добро пожаловать, {user.username}!')  # Приветственное сообщение
            return redirect('product_list')  # Перенаправление на главную страницу
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})





def user_login(request):
    # Проверка, если пользователь уже аутентифицирован
    if request.user.is_authenticated:
        logout(request)  # Выход пользователя

        return redirect('product_list')  # Перенаправление на страницу входа

    # Инициализация формы
    form = CustomUserLoginForm()
    context = {
        'form': form,
        'welcome_message': 'Добро пожаловать! Пожалуйста, войдите в свою учетную запись.',
        'error_message': None,
    }

    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('product_list')  # Перенаправление страницу или другой URL
            else:
                context['error_message'] = "Неверное имя пользователя или пароль."  # Сообщение об ошибке
        else:
            context['error_message'] = "Пожалуйста, исправьте ошибки в форме."

    context['form'] = form  # Обновляем форму в контексте, если она была отправлена
    return render(request, 'login.html', context)

