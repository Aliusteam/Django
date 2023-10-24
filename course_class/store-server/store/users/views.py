from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView

from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
# auth - для подтверждение подлинности authenticate
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from products.models import Basket
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'

# Для регистрации пользователя
class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    # Когда вы создаете новый объект модели с помощью CreateView, вам нужна форма, которая будет отображаться на странице и собирать данные от пользователя. Параметр form_class позволяет указать конкретный класс формы, который будет использоваться.
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    # Параметр success_url в классе CreateView в Django используется для определения URL-адреса, на который будет выполнен редирект после успешного создания нового объекта модели.
    success_url = reverse_lazy('users:login')
    # Выводим сообщение
    success_message = 'Вы успешно зарегистрированы!'
    title = 'Store - Регистрация'

    # def get_context_data(self, **kwargs):
    #     context = super(UserRegistrationView, self).get_context_data()
    #     # context['title'] = 'Store - Регистрация'
    #     return context


# Отображение пользовательского кабинета
class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    # Для перекидывания на ту же страницу при смене данных в профиле
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     # context['title'] = 'Store - Личный кабинет'
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context


# Для выхода из профиля
class UserLogoutView(LogoutView):
    next_page = '/'


# Для подтверждения емейла при регистрации
class EmailVerificationView(TitleMixin ,TemplateView):
    title = 'Store - подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    # Это если юзер подтверждает свой емейл, он переходит на страницу
    def get(self, request, *args, **kwargs):
        # Такие данные получаем - kwargs: {'email': ' ivan@ya.ru ', 'code': UUID('73804d42-8a3e-4267-b0ff-47d80a75fd00')}
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        # user = User.objects.filter(email=kwargs['email']).order_by('-id').first()
        # email_verifications: <QuerySet []>
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        # Если email_verifications -не пустой и время не истекло
        if email_verifications.exists() and not email_verifications.first().is_expired():  # Если список не пустой
            # Выставляем, что юзер подтвердил свою почту
            user.is_verified_email = True
            user.save()  # Сохраняем обьект с новыми данными
            # И выводим шаблон о выполнении
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))




# def login(request):
#     # Вначале проверяется какой запрос пришел
#     if request.method == 'POST':
#         # Заполняем форму - данными, которые были отправлены
#         # такие как name, password и тд.
#         # Данные сохраняются в словарь {'username':'ИМЯ', ...}
#         form = UserLoginForm(data=request.POST)
#         # Если данные имя и пароль - валидные, то проверим
#         # Есть ли у нас такой пользователь с таким паролем
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             # то делаем подтверждение подлинности - authenticate
#             user = auth.authenticate(username=username, password=password)
#             if user:  # Если такой пользователь есть, мы его авторизуем
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     # Для формы создаем контекст form и вызываем класс UserLoginForm
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

# Пользовательский личный кабинет
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         # instance=request.user - это заполняются поля данными человека
#         # который зашел в личный кабинет
#         form = UserProfileForm(instance=request.user)
#
#     context = {'title': 'Store - Профиль',
#                'form': form,
#                'baskets': Basket.objects.filter(user=request.user),
#                }
#     return render(request, 'users/profile.html', context)





# def registration(request):
#     if request.method == 'POST':
#         # Получили словарь с данными пользователя
#         form = UserRegistrationForm(data=request.POST)
#         # Проврка, что написаны правильно поля формы
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)