from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


#  Форма для отправки писем
class CotactForm(forms.Form):
    # Тема письма subject
    subject = forms.CharField(label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content - текст письма, rows : 5 - 5 рядом текст.
    content = forms.CharField(label='Текст',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


# Форма для Аутентификации пользователя, то есть, что бы Логинился
class UserLoginForm(AuthenticationForm):
    # Нам потребуются 2 поля username и password
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    # class Meta - не нужен, так как в AuthenticationForm - нет его, если перейти в него


# Это как будет отображаться форма при регистрации
class UserRegisterForm(UserCreationForm):
    # Пропишем поля, вместо поля widgets
    username = forms.CharField(label='Имя пользователя', help_text='Поле для имени',
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение Пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(
        attrs={'class':'form-control'}))

    # В этом классе Meta будет настраивать форму
    class Meta:
        model = User  # Связываем model с User
        # Какие поля и в каком порядке представляем
        fields = ('username', 'email', 'password1', 'password2')

        # Опишем нашу форму как она должна выглядеть
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        # }

# Это форма связанная с Моделью News при добавлении новости
class NewsForm(forms.ModelForm):
    # Создаем Подкласс Meta
    class Meta:
        model = News  # Укажем с какой формой будет связана модель с News
        # Перечисляем поля, какоторые хотим видеть в этой форме
        # fields = '__all__' - это не рекомендованный способ
        # fields = '__all__'  # Будут представлены все поля из наше Модели,

        # А тут прописываем все поля в ручную
        fields = ['title', 'content', 'is_published', 'category']
        # Опишем нашу форму как она должан выглядеть
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    # Кастомный валидатор для title, запрет на первый символ = цифра
    def clean_title(self):
        # cleaned_data - это словарь со всеми данными (title, content..),
        # который мы получаем, когда пользователь отправляет через форму - новость

        title = self.cleaned_data['title']  # Тут мы получим строку title
        if re.match(r'\d', title):  # Если название начинается с Цифры
            raise ValidationError('Название не должно начинаться с цифры')
        return title

# для того, что бы описать форму создаем NewsForm
# он насдежуется от forms.Form
# Это форма не связанная, по этому мы это заполням
# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={"class":"form-control"}))
#     content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(
#             attrs={
#                 "class":"form-control",
#                 "rows":5
#             }))
#     is_published = forms.BooleanField(label='Опубликовано?', initial=True)
#     # MultipleChoiceField - для связаной категории: 1 ко многим
#     category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Категория',
#                                       queryset=Category.objects.all(),
#                                       widget=forms.Select(attrs={"class":"form-control"}))


