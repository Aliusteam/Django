from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

# Create your views here.
zodiac_dict = {
    'aries': 'Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).',
    'taurus': 'Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).',
    'gemini': 'Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня',
    'cancer': 'Рак - четвертый знак зодиака, Луна (с 22 июня по 22 июля).',
    'leo': 'Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).',
    'virgo': 'Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября',
    'libra': 'Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября',
    'scorpio': 'Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 н',
    'sagittarius': 'Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по',
    'capricorn': 'Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 2',
    'aquarius': 'Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 я',
    'pisces': 'Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20'
}

def index(request):
    description = list(zodiac_dict)
    data = {
        'zodiacs' : description
    }
    return render(request, 'horoscope/index.html', context=data)

def get_info_about_sign_zodiac(request, sign_zodiac: str):
    description = zodiac_dict.get(sign_zodiac)
    zodiacs = list(zodiac_dict)
    data = {
        'sign': sign_zodiac,
        'description': description,
        'zodiacs': zodiac_dict
    }
    return render(request, 'horoscope/info_zodiaс.html', context=data)

def get_info_about_sign_zodiac_by_number(request, sign_zodiac:int):
    zodiacs = list(zodiac_dict)
    if sign_zodiac > len(zodiacs):
        return HttpResponseNotFound('Неправильный порядковый номер золдиака')

    name_zodiac = zodiacs[sign_zodiac-1]
    redirect_url = reverse('horoscope-name', args=[name_zodiac])
    # redirect_url - делает такую же строку: f'/horoscope/{name_zodiac}'
    return HttpResponseRedirect(redirect_url)
