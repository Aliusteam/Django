from django.db import models
from django.urls import reverse


class Category(models.Model):
    # verbose_name - это то, что пользователь видит какое название
    title = models.CharField(max_length=255, verbose_name='Название темы')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    # Метод возвращает строку, которая будет использоваться для представления объекта
    def __str__(self):
        return self.title

    # get_absolute_url - это метод модели в Django,
    # который используется для получения URL-адреса объекта модели.
    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    # Meta это вложенный класс модели в Django, который содержит метаданные для
    # модели. Можно задавать различные свойства модели, такие как название таблицы
    # в базе данных, порядок сортировки, уникальность полей и т.д.
    class Meta:
        # Название в единственном числе
        verbose_name = 'Категория(ю)'
        # Название во множественном числе
        verbose_name_plural = 'Категории'
        ordering = ['title']  #  Задаем сортировку по полю title


# Для выведения новостей по тегу
class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название темы')
    slug = models.SlugField(max_length=50, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

# Основная модель - публикации новостей
class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название темы')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    author = models.CharField(max_length=100, verbose_name='Автор')
    # blank=True - значит, что поле не обязательно для заполнения
    content = models.TextField(blank=True)
    # auto_now_add=True - значит, что дата будет присвоена в момент публикации
    # И эту дату мы не сможем редакировать
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    # upload_to - будет публиковаться в папку photos и расперделяться по датам
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    # ForeignKey - внешний ключ, связь 1 ко многим
    # on_delete=models.PROTECT при попытке удалить объект, на который
    # ссылаются другие объекты, будет возбуждено исключение ProtectedError.
    # Если мы задаем related_name='posts', то мы можем обращаться к
    # связанным объектам через свойство posts ,то есть так будет называться связь
    # между Post и Category, то есть у Category появится свойство posts
    # сategory = Category.objects.get(pk=1)
    # сategory.posts.all()
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='posts')
    # Связь многие ко многим, у одного поста может быть много тегов
    # Django создать доп таблицу для связи многие ко многим
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']  # Сортировка в обратном порядке













