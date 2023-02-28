from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import News, Category




class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    # Создаем поле для поиска по полям 'title', 'content'
    search_fields = ('title', 'content')
    # Указываем поле которе мы хотим редактировать в админке
    list_editable = ('is_published', )
    # Указываем по каким полям мы хотим фильтровать
    list_filter =  ('is_published', 'category')
    # Для вывода категорий при изменении новости
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')

    def get_photo(self, obj):
        # mark_save Получает строку и не эеранирует ее
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    # Обязательно в конце: запятая

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'





















