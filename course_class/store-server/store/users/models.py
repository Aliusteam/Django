from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


# Так как в django по умолчанию имеется табличка User,
# то мы наследуемся от этой таблички, что бы не запонять поля
class User(AbstractUser):
    # Добавим фотографию в модель User, то есть мы расширили,
    # уже созданный по дефолту класс user
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # Подтвердил ли пользователь свою почту
    is_verified_email = models.BooleanField(default=False)

# Создадим табличку пользователей, которые подвердили свой акаунт
class EmailVerification(models.Model):
    # Для того, что бы пользователь подтвреждал свой акаунт,
    # Он будет переходить на уникальный адрес, созданный UUIDField
    code = models.UUIDField(unique=True)
    # Связываем эту модель с моделью User - по полю User.id
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # Дата подтверждения. auto_now_add - будет автоматически проставляться
    created = models.DateTimeField(auto_now_add=True)
    # Срок годности ссылики подтверждения
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    # Отправка письма для верификации
    def send_verification_email(self):
        # Перенаправляем на email_verification в urls.py и передаем параметры email, code
        # link это адрес: users/verify/ivan@ya.ru/73804d42-8a3e-4267-b0ff-47d80a75fd00/
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        # verification_link - это полная ссылка для подтверждения
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False







