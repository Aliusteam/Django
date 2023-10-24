from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView
from django.core.cache import cache

from products.models import Product, ProductCategory, Basket
from django.core.paginator import Paginator
from common.views import TitleMixin


# Создаем класс, для отображения стартовой страницы index.
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

    # Для передачи данных в контекст - get_context_data
    # Он находиться в мексине - Класс ContextMixin
    # def get_context_data(self, **kwargs):
    #     # Получаем контекст
    #     context = super(IndexView, self).get_context_data()
    #     context['title'] = 'Store'
    #     return context


# Для вывода товаров на странице products
class ProductsListView(TitleMixin, ListView):
    # С какой моделью связываем
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'
    # Метод get_queryset определяет, какие объекты будут доступны для отображения или обработки в представлении.
    # Обычно вы переопределяете get_queryset в своем классе представления, чтобы указать определенные фильтры, сортировки или условия для выборки объектов из базы данных.
    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        # Будем выводить товары, в зависимости от выбранной категории
        # path('category/<int:category_id>/' в urls.py - данные об этом, храниться
        # теперь в словаре: self.kwargs, по этому мы берем: category_id = self.kwargs
        category_id = self.kwargs.get('category_id')  # Может быть None
        # Выводим товары, в зависимости от выбраной категории, если None, то все товары
        return queryset.filter(category_id=category_id) if category_id else queryset

    # Передаем в контекст
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        # context['title'] = 'Store - Каталог'

        # # Получаем значение по ключу Кеша - REDIS используется для кеша
        # categories = cache.get('categories')
        # if not categories:
        #     context['categories'] = ProductCategory.objects.all()
        #     cache.set('categories', context['categories'], 30)
        # else:
        #     context['categories'] = categories

        context['categories'] = ProductCategory.objects.all()
        return context


# Мы не будем переводить этот метод в класс
# Это обработчик событий, при нажатии на кнопку: Отправить в корзину
# product_id - это информация, что за обьект передается
@login_required
def basket_add(request, product_id):
    # Продукт ложим в корзину
    product = Product.objects.get(id=product_id)
    # Берутся все корзины пользователя с определенным продуктом
    # Но всегда будет передаваться одby продукт и один пользователь
    baskets = Basket.objects.filter(user=request.user, product=product)

    # Проверка что корзина не существует
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    # Если товар уже добавлен в корзину
    else:
        # Так как все равно один товар в корзине, берем: first()
        basket = baskets.first()
        # Увеличиваем этот товар на 1
        basket.quantity += 1
        basket.save()
    # Перенаправляем пользователя на ту же страницу, где он находится
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Мы не будем переводить этот метод в класс
# Удаление товара из корзины
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# # Мы не будем переводить метод добавления в корзину в класс, так как он не соответсвует
# # Рекомендации для написания этого метода в Класс. То есть def basket_add - оставляем
# class BasketCreateView(CreateView):
#     model = Basket
#     # Класс CreateView в Django представляет представление, которое используется для создания новых объектов модели. Он предоставляет реализацию стандартной операции создания (создание новой записи в базе данных) и обрабатывает запросы методом POST.
#     # Когда вы отправляете форму на странице, содержащей CreateView, браузер отправляет HTTP-запрос методом POST на указанный URL. Метод POST используется для отправки данных на сервер для создания нового объекта.
#     def post(self, request, *args, **kwargs):
#         product = Product.objects.get(id=self.kwargs.get('product_id'))
#         baskets = Basket.objects.filter(user=request.user, product=product)






