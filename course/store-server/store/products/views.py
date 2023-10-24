from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import Product, ProductCategory, Basket
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


# Выводим товары, page_number=1 - это 1ая страница пагинации
def products(request, category_id=None, page_number=1):
    # Сделаем проверку, выбрал ли пользователь категорию товара
    # Или просто находится во всех  товарах
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 3  # Сколько товаров на странице отображать
    # paginator в представленном коде представляет собой объект Paginator, который используется для разбиения коллекции products на страницы.
    paginator = Paginator(products, per_page)
    # products_paginator содержит информацию о странице, и данные с products, включая сам список товаров на этой странице и другую информацию, такую как номер текущей страницы, общее количество страниц и т.д.
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator
    }
    return render(request, 'products/products.html', context)


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


# Удаление товара из корзины
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])








