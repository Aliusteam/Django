from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification
from users.forms import UserRegistrationForm


# Проверка регистрации пользователя
class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')

        self.data = {
            'first_name': 'Valerii',
            'last_name': 'Pavlikov',
            'username': 'valerii',
            'email': 'sf34fsdf@mail.ru',
            'password1': '12345678Pp',
            'password2': '12345678Pp',
        }

    # Тест при заходе на страницу регистрации - GET запрос
    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    # Тест: При отправке данных - при регистрации пользователя
    def test_user_registration_post_success(self):
        # Данные для регистрации пользователя - берутся с формы forms.py

        username = self.data['username']
        # Проверка, что изначально пользователя нет
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        # Проверим, что пользователь был создан. Что есть хоть 1 такой пользователь
        self.assertTrue(User.objects.filter(username=username).exists())

        # Проверка, что емейл проходит верификацию, для последующей отправки письма
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date()
            (now() + timedelta(hours=48)).date()
        )

    # Проверка, что username уже создан
    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.',
                            html=True)









