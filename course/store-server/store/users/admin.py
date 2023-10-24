from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
    # Мы в пользователе выведем корзину то, что у него в корзине
    # Это поле выводиться, если таблички связанные - foreign key
    inlines = (BasketAdmin, )



