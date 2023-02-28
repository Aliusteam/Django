from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, CotactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


#  Регистрация пользоветелей на сайте
def register(request):
    # Тут мы передаем заполненые данные регистрации на сервер
    # Если мы отправляем запрос на регистрацию
    if request.method == 'POST':
        # Заполняем метод данными из поста
        form = UserRegisterForm(request.POST)
        # Проводим валидацию формы
        if form.is_valid():
            # Сохраняем форму
            # Так как форма связана с моделью User, то данные сохраняться в базе
            # В переменную user - передадим данные о регистрации пользователя
            user = form.save()
            # И сразу вызовем метод Логин, что бы пользователь сразу залогинился
            login(request, user)
            # Выдаем всплывающее сообщение о регистрации
            messages.success(request, 'Вы успешно зарегистрировались')
            # Перенаправляем на стреницу Логина
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        # Будет не связанная форма
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


#  Функция для выхода из авторизации
def user_logout(request):
    #  Выходим из авторизации пользователя
    logout(request)
    #  Перенаправляем пользователя на страницу регистрации
    return redirect('login')


# cleaned_data - это словарь, который содержит обработанные и валидные данные формы,
# представленной в Django. После того, как пользователь отправляет форму,
# Django автоматически проверяет ее на наличие ошибок и помещает все введенные
# данные в словарь cleaned_data, если данные являются корректными.
def contact(request):
    if request.method == 'POST':
        # Заполняем метод данными из поста
        form = CotactForm(request.POST)
        # Проводим валидацию формы
        if form.is_valid():
            # Оптравка письма, cleaned_data - описание выше
            # Функция send_mail возвращает 1 или 0, это кол-во отправленных писем
            # mail - это результат 1 или 0
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                      'mexet777@mail.ru', ['forte.evm@mail.ru'], fail_silently=False)
            if mail:  #  Если mail = 1
                # Выдаем всплывающее сообщение Письмо отправлено
                messages.success(request, 'Письмо отправлено!')
                # Перенаправляем на стреницу Логина
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        # Будет не связанная форма
        form = CotactForm()
    return render(request, 'news/test.html', {'form': form})


# Вход по логину
def user_login(request):
    # Если запрос пришел Постом
    if request.method == 'POST':
        # Создаем экземпляр Формы и связываем его form с данными
        # Без присовения data=request.POST - Работать не будет
        # Получается, что мы ссылаемся на UserLoginForm, который
        # у нас создан в forms.py
        form = UserLoginForm(data=request.POST)
        # Если форма валидна
        if form.is_valid():
            #  Нам нужно авторизовать пользователя
            #  Вначале получаем пользователя
            user = form.get_user()
            # Можем развивать метод login
            # Получить запрос request и авторизованного пользователя user
            # Получается, что пользователь авторизовался успешно
            login(request, user)
            # Теперь перенаправим пользователя
            return redirect('home')
    else:
        #  Если данные пришли не постом
        #  Создаем форму не связанную с данными
        form = UserLoginForm()
    # В конекте передадим форму {'form': form}
    return render(request, 'news/login.html', {'form': form})

# Получение всех новостей на главной странице
class HomeNews(MyMixin, ListView):
    # Переобпределим атрибуты
    # Это тоже самое, что news = News.objects.all(), то есть получим все данные модели
    model = News
    # Это не обязательно, но можно переопределить шаблон
    template_name = 'news/home_news_list.html'
    # Это то, что мы указываем в шаблоне - news
    # А именно переменую обьекта, что бы в шаблоне не менять название
    context_object_name = 'news'
    # Для передачи статических данных
    # extra_context = {'title': 'Главная'}  # метод не рекомендован
    # mixin_prop - определим еще одно свойство из Миксин в наш класс
    mixin_prop = 'hello world'
    # Сделаем пагинацию по 2 записи на странице
    # Это ограничивает количество объектов на странице и
    # добавляет paginator и page_obj к context
    paginate_by = 2

    # Рекомендованный метод для передачи данных 
    def get_context_data(self, *, object_list=None, **kwargs):
        # мы сохранили все данные, которые были в context
        context = super(HomeNews, self).get_context_data(**kwargs)
        # Теперь дополним context
        context['title'] = self.get_upper('главная страница')
        # Передаем в context - наш Миксин, а именно его функцию get_prop
        context['mixin_prop'] = self.get_prop()
        # возвращаем context
        return context

    # Для фильтрации какие новости публиковать
    def get_queryset(self):
        return News.objects.filter(is_published=True)

# Получение категорий
class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # Запретим показывать новости в категориях, где нет новостей
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Укажем, что выводить только те новости, у которых категория = category_id
        # context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        # возвращаем context
        return context

    # Для того, что бы вывести все новости конкретной категории,
    # указываем: category_id=self.kwargs['category_id']
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True)

# Получение конкретной новости
class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    # slug_url_kwarg - Для указания по слагу
    # template_name = 'news/news_detail.html'

    # Что бы не менять это название в шаблоне, указываем тут
    context_object_name = 'news_item'


# Создание формы добавления новостей
class CreateNews(LoginRequiredMixin, CreateView):
    # Нужно связать данный класс CreateNews с формой NewsForm
    form_class = NewsForm
    # Укажем шаблон для формы
    template_name = 'news/add_news.html'
    # На какую старничку перебрасывать при создании новости
    # success_url = reverse_lazy('home')

    # login_url перебрасывает на страницу админа, если запрещен
    # доступ для неавторизированных пользователей
    # Это при работе миксина - LoginRequiredMixin
    login_url = '/admin/'
    # Перебрасываем на ошибку для для неавторизированных пользователей
    raise_exception = True


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context=context)

# def get_сategory(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk = category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'news/category.html', context=context)

# # Получение конкретной новости
# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item,
#     }
#     return render(request, 'news/view_news.html', context=context)
#
# def add_news(request):
#     # Если метод передачи данных будет как POST, а не ГЕТ,
#     # То есть если мы отправляем данные ФОРМЫ, а не получаем
#     if request.method == 'POST':
#         # Форма была отправлена
#         form = NewsForm(request.POST)
#         # Смотрим, что прошла ли форма валидацию
#         if form.is_valid():
#             # cleaned_data - это словарь, где сохраняется вся информация об отправленой новости
#             # print(form.cleaned_data)
#             # Тут мы сохраняем данные новости в нашу модель News
#             # ** обозначает, что Питон распакует словарь с данным добавленной новости cleaned_data
#             # То есть ** присвоит переменные словаря по ключам и значениям
#             # news = News.objects.create(**form.cleaned_data)  # Этот метод сохранения для НЕ Связаной формы
#             news = form.save()   # Этот метод сохранения для Связаной формы
#             # return redirect('home') # Переход на главную страницу
#             return redirect(news)  # Переход на саму новость
#
#     # а тут если человек просто зашел на страничку формы
#     else:
#         form = NewsForm()  # Тут передается НЕ Связанная форма с данными
#     return render(request, 'news/add_news.html', {'form': form})
