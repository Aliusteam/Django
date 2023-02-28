from django.contrib import admin
from .models import Movie
from django.db.models import QuerySet
# Register your models here.


class RatingFilter(admin.SimpleListFilter):
    title = 'фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('от 40 до 59', 'Средний'),
            ('от 60 до 79', 'Высокий'),
            ('>=80', 'Высочайший'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value() == 'от 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        if self.value() == '>=80':
            return queryset.filter(rating__gte=80)
        # return queryset.all()

@admin.register(Movie)  # способ регистрации №2
class MovieAdmin(admin.ModelAdmin):
    # fields = ['name', 'rating']
    # exclude = ['slug']
    # readonly_fields = ['year']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name','rating','year', 'budget', 'currency', 'rating_status']
    list_editable = ['rating', 'year', 'budget', 'currency']
    ordering = ['-rating']
    actions = ['set_dollars', 'set_euro']
    search_fields = ['name']
    list_filter = ['name', 'currency', RatingFilter]

    @admin.action(description='Установить валюту в доллар')
    def set_dollars(self, requests, qs: QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Установить валюту в евро')
    def set_euro(self, requests, qs: QuerySet):
        count_updated = qs.update(currency=Movie.EUR)
        self.message_user(
            requests,
            f'Было обновлено {count_updated} записей'
        )

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Зачем это смотреть?'
        if mov.rating < 70:
            return 'Разок можно глянуть'
        if mov.rating <= 85:
            return 'Зачет'
        return 'Топчик'

# admin.site.register(Movie, MovieAdmin)