import stripe

from django.db import models
from django.conf import settings

from users.models import User


stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        # Это как будет отображаться в админке данная табличка
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    # max_digits - сколько чисел до запятой
    # decimal_places - сколько чисел после запятой
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # quantity - количество товара
    # PositiveIntegerField - только положительные целый числа
    quantity = models.PositiveIntegerField(default=0)
    # upload_to - куда будут сохраняться изображения
    image = models.ImageField(upload_to='products_images')
    # stripe_product_price_id - для передачи в stripe - id заказа
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    # В подсказках выдается "to" - это с чем связываем
    # on_delete - что делать при удалении
    # CASCADE - при удалении категории, удаляются и все товары с этой категорией
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        # Это как будет отображаться в админке данная табличка
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    # Метод для добавления stripe_product_price_id для каждого сохраненого товара
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Сдесь добавляем логику, до вывода основного метода super
        # Если на товар не получили id товара для stripe
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

    # Этот метод создает в Страйп цену продукта и сам продукт
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency="rub",
        )
        return stripe_product_price

#  Этот класс - нам для добавления методов total_sum и total_quantity
# Что бы работать с методами:
# baskets = Basket.objects.filter(user = user)
# baskets.total_sum() или baskets.total_quantity()
class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        # baskets = Basket.objects.filter(user=self.user)
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        # baskets = Basket.objects.filter(user=self.user)
        return sum([basket.quantity for basket in self])

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


# Это наша корзина товара
class Basket(models.Model):
    # Соединяем по внешнему ключу с моделью User
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    # Для отображения даты и времени, auto_now_add - поле
    # всегда будет создаваться при создании нового обьекста
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # Переопределим метод objects, который является главным методом,
    # с помощью которого делаются: Basket.objects.all() и др.
    # Мы его получаем из созданого нами BasketQuerySet (указан выше)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    # Для отображения суммы товара в корзине
    def sum(self):
        return self.product.price * self.quantity

    # Будет возвращать данные корзины в json формате
    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item


    # def total_sum(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum([basket.sum() for basket in baskets])
    #
    # def total_quantity(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum([basket.quantity for basket in baskets])









