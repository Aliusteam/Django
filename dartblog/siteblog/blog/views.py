from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from django.db.models import F, Q


class Home(ListView):
    # Переобпределим атрибуты
    # Это тоже самое, что news = Post.objects.all(),
    # то есть получим все данные из модели
    model = Post
    # Это не обязательно, но можно переопределить шаблон
    template_name = 'blog/index.html'
    # Обьект, который будет заполняться данными, это то,
    # что мы будем указывать в шаблоне - posts
    context_object_name = 'posts'
    # Сделаем пагинацию по 2 записи на странице
    # Это ограничивает количество объектов на странице и
    # добавляет paginator и page_obj к context
    paginate_by = 4

    # Рекомендованный метод для передачи данных
    # get_context_data - мы можем не только передать в контексте данные,
    # но также можем с данными работать
    def get_context_data(self, *, object_list=None, **kwargs):
        # Сохраним все данные, которые были в context, что бы не потерять
        context = super().get_context_data(**kwargs)
        # Дополним context
        context['title'] = 'Classsic Blog Design'
        # Возвращаем context
        return context


class PostsByCategory(ListView):
    # определять model у нас особого смысла нет, так мы его и так
    # будем получать через get_queryset, где и будет испозоваться Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    # Что бы при переходе на несуществующую категорию, была ошибка
    allow_empty = False

    # Метод get_queryset() возвращает объект QuerySet, который представляет собой запрос к
    # базе данных для извлечения данных. Чтобы определить набор данных, который нужно
    # получить для отображения на странице.
    # Тут мы связываем PostsByCategory с моделью Сategory по полю category
    def get_queryset(self):
        # Модель Post во вторичной модели ссылается по category - внешнего ключа,
        # на slug - в первичной модели Category: category__slug
        # И затем сравниваем все новости у которых slug = запрашиваемой категории
        # self.kwargs['slug'] - это способ получить значение переменной slug,
        # переданной через URL-адрес в urls.py
        return Post.objects.filter(category__slug=self.kwargs['slug'])
        # Можно и так:
        # return Category.objects.filter(slug=self.kwargs['slug'])

        # get_context_data - это метод класса в Django, который используется для
        # получения и формирования дополнительных данных, которые будут переданы в
        # шаблон вместе с основными данными.
    def get_context_data(self, *, object_list=None, **kwargs):
        # Сохраним все данные, которые были в context, что бы не потерять
        context = super().get_context_data(**kwargs)
        # Дополним context
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        # Возвращаем context
        return context


# Для публикации конкретной новости
class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'


    def get_context_data(self, *, object_list=None, **kwargs):
        # Сохраним все данные, которые были в context, что бы не потерять
        context = super().get_context_data(**kwargs)
        # F - это класс в модуле django.db.models, который позволяет обращаться к полям
        # модели базы данных внутри выражений запросов. Здесь мы используем F('views') для
        # обращения к значению поля views внутри самого запроса, модели Post
        # Получим сколько раз просматривали новость и прибавим 1
        self.object.views = F('views') + 1
        # Это все нам нужно сохранить
        self.object.save()
        # Теперь просто так мы не можем использовать views, нам нельзя использовать,
        # потому что там будет выражение и нам нужно перезапросить данные из базы данных
        self.object.refresh_from_db()
        return context


# Выборка по тэгу
class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тэгу: ' + str(
                        Tag.objects.get(slug=self.kwargs['slug']))
        return context


# Для поиска статей на сайте, запрос по слову, которую введут пользователь
class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # icontains - регситро независемый посик для латиницы,
        # для кирилицы - регситро зависемый
        # GET - массив, get('s') - это функция, которая забирет данные, мы из
        # указали в шаблоне single.html: name="s"
        # То есть мы передаем сюда строку для поиска, которую введет пользователь
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))
        # Что бы фильтровать сразу по title и content:
        # return Post.objects.filter(
        #     Q(title__icontains=self.request.GET.get('s')) |
        #     Q(content__icontains=self.request.GET.get('s'))
        # )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем параметр s, который был у нас в search.html,
        # что бы работала постраничная пагинация при поиске
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context




# def index(request):
#     return render(request, 'blog/index.html')
#
# # Для теста, получим ссылки на категории
# def get_category(request, slug):
#     return render(request, 'blog/category.html')
#
# def get_post(request, slug):
#     return render(request, 'blog/category.html')
















