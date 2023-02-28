from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    # blank=True - Необязательный для заполнения
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    # auto_now_add=True - дата новости будет создана 1 раз и меняться не будет при обновлении
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    # uto_now=True - дата будет обновляться при обновлении записи
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото',blank=True)
    # upload_to='photos/%Y/%m/%d' - будут сохраняться фото по этому пути
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    # Для связи модели News с class Category
    # on_delete=models.PROTECT - Не дает удалить категорию связанных данных
    # То есть при удалении категории - не удаляться новости
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    views = models.IntegerField(default=0)


    def get_absolute_url(self):
        # view_news - мы берем из urls.py - это: name='view_news'
        # news_id - мы берем из urls.py - это: 'news/<int:news_id>/
        return reverse('view_news', kwargs={'news_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        # Заменяем названия в админке
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        # Сортировка в админке и в пользовательской части
        ordering = ['-created_at', 'title']

# Создаем модель Category - для связи один ко многим
class Category(models.Model):
    # db_index = True - Делает индексацию по этому полю, для более быстрого поиска
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    # для построения ссылок на категории - это считается рекомендуемым построением
    def get_absolute_url(self):
        # Такое же построение как у нас в urls.py
        # Это посмтроение похоже на тег URL: {% url 'сategory' item.pk %}
        # reverse в python и тег URL в html - делают одно и тоже
        return reverse('сategory', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']













