from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.blog),
    path('<int:sign_zodiac>', views.get_int_zodiac),
    path('<str:sign_zodiac>', views.get_str_zodiac, name='sign-name'),
]