from django.urls import path
from news.views import *
# Для кэша:
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('', index, name='home'),
    # Кеширование страницы cache_page
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>/', get_сategory, name='сategory'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='сategory'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
]












