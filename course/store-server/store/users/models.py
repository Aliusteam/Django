from django.db import models
from django.contrib.auth.models import AbstractUser

# Так как в django по умолчанию имеется табличка User,
# то мы наследуемся от этой таблички, что бы не запонять поля
class User(AbstractUser):
    # Добавим фотографию в модель User, то есть мы расширили,
    # уже созданный по дефолту класс user
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
