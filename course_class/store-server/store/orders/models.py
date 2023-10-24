from django.db import models

from users.models import User
from products.models import Basket


# Заказ
class Order(models.Model):
    # Статусы заказа
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен')
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    # Статус берется из выше переменных статусов
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    # Это пользователь, который оформил заказ
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    # Берем последний раз корзину, что бы сохранить ее в истории
    # обновление после оплаты
    def update_after_payment(self):
        # получаем корзину пользователя, который оформлял заказ
        baskets = Basket.objects.filter(user=self.initiator)
        # Меняем статус на оплачен
        self.status = self.PAID
        # Получаем все оплаченные товары и помещаем их в историю
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        # Удаляем корзины с товаром
        baskets.delete()
        self.save()




