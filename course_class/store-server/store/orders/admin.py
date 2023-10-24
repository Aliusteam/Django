from django.contrib import admin

from orders.models import Order


# Регистрируем в Админке
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display является атрибутом класса ModelAdmin, используемым для определения полей модели, которые должны быть отображены в списке объектов модели в административной панели
    # __str__ - это мы отображаем, что будет как в выводе __str__
    list_display = ('__str__', 'status')
    fields = (
        'id', 'created', ('first_name', 'last_name'), ('email', 'address'),
        'basket_history', 'status', 'initiator'
    )
    # Что нельзя менять
    readonly_fields = ('id', 'created')
