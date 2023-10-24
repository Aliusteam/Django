from django.contrib import admin
from products.models import ProductCategory, Product, Basket


# Регистрация наших моделей models
# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)  # Указываем с какой моделью будет работать
class ProductAdmin(admin.ModelAdmin):
    # Это поля, которые будут отображаться в админке
    list_display = ('name', 'price', 'quantity', 'category')
    # Это поля, которые указываются в самом товаре
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'stripe_product_price_id', 'category')
    # Сделаем поля товара только для чтения
    readonly_fields = ('description', )
    # Поиск по полю
    search_fields = ('name', )
    # Сортировка по полю
    ordering = ('-name', )


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0













