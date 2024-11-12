from django.shortcuts import render
from . models import Author, Category, Recipe
import logging


logger = logging.getLogger(__name__)


def index(request):
    context = {'title': 'Главная страница',
               'content': 'Здравствуйте, добро пожаловать на главную страницу сайта',
               }
    logger.debug('открытие стартовой страницы')

    return render(request, 'my_app/index.html', context)
