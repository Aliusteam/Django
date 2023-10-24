from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User

# Для того, что бы пользователь залогинился
# Наследуемся от готовой формы AuthenticationForm
class UserLoginForm(AuthenticationForm):
    # Для красоивой формы, нам нужно добавить несколько виджетов
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




