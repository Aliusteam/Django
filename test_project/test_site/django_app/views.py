from django.shortcuts import render, redirect
from .models import HomeMenu


def category_id(request, pk):
    context = {
        'pk': pk,
        'menu': HomeMenu.objects.all()
    }
    return render(request, 'django_app/index.html', context=context)


def start(request):
    return redirect('/1/')


