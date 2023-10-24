from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
# auth - для подтверждение подлинности authenticate
from django.contrib import auth, messages
from django.urls import reverse
from products.models import Basket


def login(request):
    # Вначале проверяется какой запрос пришел
    if request.method == 'POST':
        # Заполняем форму - данными, которые были отправлены
        # такие как name, password и тд.
        # Данные сохраняются в словарь {'username':'ИМЯ', ...}
        form = UserLoginForm(data=request.POST)
        # Если данные имя и пароль - валидные, то проверим
        # Есть ли у нас такой пользователь с таким паролем
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # то делаем подтверждение подлинности - authenticate
            user = auth.authenticate(username=username, password=password)
            if user:  # Если такой пользователь есть, мы его авторизуем
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    # Для формы создаем контекст form и вызываем класс UserLoginForm
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        # Получили словарь с данными пользователя
        form = UserRegistrationForm(data=request.POST)
        # Проврка, что написаны правильно поля формы
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        # instance=request.user - это заполняются поля данными человека
        # который зашел в личный кабинет
        form = UserProfileForm(instance=request.user)

    context = {'title': 'Store - Профиль',
               'form': form,
               'baskets': Basket.objects.filter(user=request.user),
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
