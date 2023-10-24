from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from products.models import Product, ProductCategory

class IndexViewTestCase(TestCase):

    def test_view(self):
        # Имитируем, что пользователь зашел на сайт
        path = reverse('index')  # 'http://127.0.0.1:8000/'
        response = self.client.get(path)

        # Проверка, что 1ый параметр будет равен второму
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    # Так как QuerySet у нас будет пустой, так как у нас при тестах -
    # создается тестовая база - пустая. То мы загрузим данные из fixtures
    fixtures = ['categories.json', 'goods.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()

    # Этот тест для выведения всех товаров на 1 странице = 3 товара всего
    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        # products - это QuerySet из нашего проекта
        # products = Product.objects.all()

        self._comon_tests(response)
        # Сравиваем QuerySet тестовой таблички и табличкей нашей базы данных
        # Используем list() - для того, что бы QuerySet был переведем в Список для сравнения
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    # Это тест на вывод товаров по категории
    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        # products = Product.objects.all()

        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._comon_tests(response)

        self.assertEqual(list(response.context_data['object_list']),
                         list(self.products.filter(category_id=category.id)))

    def _comon_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

