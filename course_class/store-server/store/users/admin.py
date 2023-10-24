from django.contrib import admin

from users.models import User, EmailVerification
from products.admin import BasketAdmin

# admin.site.register(User)
# Это то, что у нас будет отображаться в админке
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
    # Мы в пользователе выведем корзину то, что у него в корзине
    # Это поле выводиться, если таблички связанные - foreign key
    inlines = (BasketAdmin, )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )












