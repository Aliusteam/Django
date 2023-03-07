from django.urls import path
from .views import category_id, start


urlpatterns = [
    path('<int:pk>/', category_id, name='category_id'),
    path('', start, name='start'),
]