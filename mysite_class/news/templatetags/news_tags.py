from django import template
from django.db.models import Count
from django.core.cache import cache

from news.models import Category


# Регистрируем наш тег
register = template.Library()

@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()

# Мы рендерим этот шаблон list_categories.html и отдаем данные
@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # # Мы Получаем (get) категории из Кэша
    # categories = cache.get('categories')
    # if not categories:
    # # categories = Category.objects.all()
    # # Тут мы фильтруем, что бы в категории была хоть 1 новость
    #     categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    #     # Теперь кэшируем категории
    #     cache.set('categories', categories, 30)
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {"categories": categories}






