import uuid
from datetime import timedelta

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.utils.timezone import now

from users.models import User, EmailVerification
from users.tasks import send_email_verification


# Для того, что бы пользователь залогинился
# Наследуемся от готовой формы AuthenticationForm
class UserLoginForm(AuthenticationForm):
    # Для красивой формы, нам нужно добавить несколько виджетов
    # Переопределим 2 поля.
    # 'class': 'form-control py-4' и 'placeholder': 'Введите имя пользователя'
    # берем из login.html именно из <input (где мы расскоментировали)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'
    }))
    #  Сначала создаем Meta, потом forms.CharField(widget...
    class Meta:
        # Данная форма будет работать с моделью пользователей
        model = User
        # а именно с полями : 'username', 'password'
        fields = ('username', 'password')


# Для регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    # 2. Кастомизируем форму
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))
    # 1. Начинаем с Мета
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',  'password1', 'password2')

    # save - обрабатывается, когда создается обьект пользователя. Оптравляем письмо
    def save(self, commit=True):
        # save - возвращает обьекст user
        user = super(UserRegistrationForm, self).save(commit=True)
        # Выставляем дату окончания действия кода подвреждения
        # expiration = now() + timedelta(hours=48)
        # # record - запись. То есть мы обьект создали create
        # record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        # # Отправляем письмо с подверждением (метод создали в models)
        # record.send_verification_email()

        # delay - это метод для паралельной работы, асинхронной
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-label'}))
    # readonly = True - это поле мы ставим не изменяемым
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'readonly':True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'readonly':True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')




