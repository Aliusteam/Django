from django import template
from blog.models import Category

# Регистрируем библиотеку
register = template.Library()

# inclusion_tag - это второй тег, первый это simple_tag
# @ - вывели декоратор
@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(menu_class='menu'):
    # Так как повторение кода в розделе Категория
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_class}











