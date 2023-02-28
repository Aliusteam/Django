from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError


# Это форма связанная с Моделью News
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


