from django import template
from django_app.models import Menu

register = template.Library()

@register.simple_tag
def draw_menu(menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return ""

    items = menu.items.all()

    # выводите меню в нужном формате, например, используя шаблонизатор
    return " ".join([f"<a href='{item.url}'>{item.title}</a>" for item in items])
