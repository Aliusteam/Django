from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm
from django.core.paginator import Paginator


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6']
    paginator = Paginator(objects, 2)  # Делаем пагинацию по 2 новостям на странице
    # Получим номер текущей страницы page_num
    # Если нет параметра page, то подставить 1
    page_num = request.GET.get('page', 1)
    # Получим обьекты - новости, которые есть на запрашиваемой странице
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})

def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    return render(request, 'news/index.html', context=context)

def get_сategory(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk = category_id)
    context = {
        'news': news,
        'category': category
    }

    return render(request, 'news/category.html', context=context)

# Получение конкретной новости
def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'news_item': news_item,
    }
    return render(request, 'news/view_news.html', context=context)

def add_news(request):
    # Если метод передачи данных будет как POST, а не ГЕТ,
    # То есть если мы отправляем данные ФОРМЫ, а не получаем
    if request.method == 'POST':
        # Форма была отправлена
        form = NewsForm(request.POST)
        # Смотрим, что прошла ли форма валидацию
        if form.is_valid():
            # cleaned_data - это словарь, где сохраняется вся информация об отправленой новости
            # print(form.cleaned_data)
            # Тут мы сохраняем данные новости в нашу модель News
            # ** обозначает, что Питон распакует словарь с данным добавленной новости cleaned_data
            # То есть ** присвоит переменные словаря по ключам и значениям
            # news = News.objects.create(**form.cleaned_data)  # Этот метод сохранения для НЕ Связаной формы
            news = form.save()   # Этот метод сохранения для Связаной формы
            # return redirect('home') # Переход на главную страницу
            return redirect(news)  # Переход на саму новость

    # а тут если человек просто зашел на страничку формы
    else:
        form = NewsForm()  # Тут передается НЕ Связанная форма с данными
    return render(request, 'news/add_news.html', {'form': form})
