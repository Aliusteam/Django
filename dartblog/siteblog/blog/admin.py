from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# PostAdminForm - это пользовательская форма администратора Django,
# которая наследуется от стандартной формы модели forms.ModelForm.
# Эта форма позволяет определить, как поля модели будут отображаться в административной
# панели Django. Вы можете определить свои собственные валидаторы формы, изменить виджеты
# полей, а также добавить свои собственные поля в форму.
# PostAdminForm может использоваться для настройки формы, используемой при создании или
# редактировании объектов модели Post в административной панели Django. Например,
# вы можете добавить дополнительное поле, которое не существует в модели Post,
# но необходимо для вашего приложения.
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

# class PostAdmin - это класс, который определяет настройки для административного
# интерфейса Django для модели Post. Он используется для настройки отображения модели
# в административном интерфейсе, включая поля, которые будут отображаться в списке и
# на странице редактирования, фильтры и поиск.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    # Для удобной публикации новостей через админку
    # save_as = True
    # Для отображения панели публикации новости
    save_on_top = True
    # list_display - это атрибут административной модели Django, который определяет, какие
    # поля модели будут отображаться в списке записей этой модели в административной панели.
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'get_photo', 'views')
    # Сделаем, что бы 'id', 'title' отображались как ссылки
    list_display_links = ('id', 'title')
    # Сделаем возможность поиска
    search_fields = ('title',)
    # Сделаем фильтр для отбора
    list_filter = ('category', 'tags')
    # Поля только для чтения
    readonly_fields = ('views', 'created_at', 'get_photo')
    # Поля которые показывать внутри создания новости
    fields = ('title', 'slug', 'category', 'tags', 'content',
              'photo', 'get_photo','views', 'created_at')

    # Создадим функцию, которая будет выводить фото в админке
    def get_photo(self, obj):
        # mark_safe - это функция в Django, которая используется для пометки строки как
        # безопасной и предотвращения ее автоматического экранирования при выводе на
        # странице. Это может быть полезно, если вы выводите HTML-код на странице и не
        # хотите, чтобы он был экранирован или выведен как текст.
        if obj.photo:  # Если есть фото
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    # Что бы в админке, отображалось название Фото
    get_photo.short_description = 'Фото'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)





