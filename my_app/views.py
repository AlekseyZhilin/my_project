from django.db.models import Count
from django.shortcuts import render
from . models import Author, Category, Recipe
from . forms import SelectPramForm, CategoryForm
import logging


logger = logging.getLogger(__name__)


def index(request):
    context = {'title': 'Главная страница',
               'content': 'Здравствуйте, добро пожаловать на главную страницу сайта',
               }
    logger.debug('открытие стартовой страницы')

    return render(request, 'my_app/index.html', context)


def show_authors(request):
    authors = Author.objects.all()
    context = {'title': 'Список авторов',
               'authors': authors
               }
    return render(request, 'my_app/show_authors.html', context)


def count_recipe_author(request):
    if request.method == 'POST':
        form = SelectPramForm(request.POST)
        if form.is_valid():
            count_recipe = form.cleaned_data['count_recipe']
            query_res = (Recipe.objects.values('authors__name').annotate(total=Count('pk'))
                         .filter(total__gte=count_recipe, published__exact=True)
                         .order_by('-total'))
            content = {
                'title': 'Количество рецептов автора',
                'query_res': query_res,
            }
            logger.debug('Количество рецептов автора получено')
            return render(request, 'my_app/count_recipe_author.html', content)

    form = SelectPramForm()
    content = {'title': 'SelectParam',
               'form': form,
               }
    return render(request, 'my_app/enter_param_form.html', content)


def show_categories(request):
    categories = Category.objects.all()
    context = {'title': 'Список категорий',
               'categories': categories
               }
    return render(request, 'my_app/show_categories.html', context)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']

            value_in_db = Category.objects.values('title').filter(title=title).first()
            if value_in_db is None:
                category = Category(title=title, description=description)
                category.save()
                message = f'Категория {title} сохранена'
            else:
                message = f'Категория {title} уже существует'
        else:
            message = f'Не верные данные'
        logger.debug(message)
    else:
        form = CategoryForm()
        message = 'Заполните данные'

    return render(request, 'my_app/enter_param_form.html', {'form': form, 'message': message})
