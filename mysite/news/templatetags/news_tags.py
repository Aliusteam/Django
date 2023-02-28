from django import template
from django.db.models import Count

from news.models import Category


# Регистрируем наш тег
register = template.Library()

@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()

# Мы рендерим этот шаблон list_categories.html и отдаем данные
@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    # Тут мы фильтруем, что бы в категории была хоть 1 новость
    # categories = Category.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {"categories": categories}
