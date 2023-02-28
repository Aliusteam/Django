from django.urls import path
from news.views import *

urlpatterns = [
    path('test/', test, name='test'),
    path('', index, name='home'),
    path('category/<int:category_id>/', get_сategory, name='сategory'),
    path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/add-news/', add_news, name='add_news'),
]
