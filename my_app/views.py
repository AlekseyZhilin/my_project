from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render, redirect
from .models import Author, Category, Recipe, Item
from .forms import SelectPramForm, AuthorForm, CategoryForm, RecipeForm, ItemForm
from django.contrib.auth import authenticate, login
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    context = {'title': 'Аутентификация пользователя',
               'message': 'Аутентификация пользователя'
               }

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'my_app/login_form.html', context)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        logger.info(f'Пользователь {username} зарегистрировался')
        return redirect('/')

    logger.info(f'Ошибка аутентивикации {username}')
    context['message'] = 'Ошибка аутентификации'
    return render(request, 'my_app/login_form.html', context)


def index(request):
    logger.debug('открытие стартовой страницы')

    recipes = Recipe.objects.all()[:5]
    context = {'title': 'Главная страница',
               'context': 'Здравствуйте, добро пожаловать на главную страницу сайта',
               'columns': ('Наименование', 'Описание', 'Время приготовления', 'Опубликован', 'Создан', 'Изменить', 'Удалить'),
               'recipes': recipes
               }

    return render(request, 'my_app/index.html', context)


def show_authors(request):
    authors = Author.objects.all()
    context = {'title': 'Список авторов',
               'context': 'Список авторов',
               'columns': ('Имя', 'Возраст', 'Почта'),
               'authors': authors
               }
    return render(request, 'my_app/show_authors.html', context)


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            description = form.cleaned_data['description']

            try:
                author = Author(name=name, email=email, age=age, description=description)
                author.save()
                message = f'Автор {name} записан'
                logger.info(message)
                return redirect('/authors/show')
            except IntegrityError as err:
                logger.warning(err)
                message = f'Имя {name} уже существует'
            except Exception as err:
                logger.warning(err)
                message = 'Данные не сохранены'

        else:
            message = 'Неточные данные'
            logger.info(message)

    else:
        form = AuthorForm()
        message = 'Заполните данные автора'

    context = {'form': form,
               'title': 'AddAuthors',
               'message': message,
               }
    return render(request, 'my_app/enter_param_form.html', context)


def count_recipe_author(request):
    if request.method == 'POST':
        form = SelectPramForm(request.POST)
        if form.is_valid():
            count_recipe = form.cleaned_data['count_recipe']
            query_res = (Author.objects.values('name').annotate(total=Count('id'))
                         .filter(total__gte=count_recipe, authors__published__exact=True)
                         .order_by('-total'))
            content = {
                'title': 'Количество рецептов автора',
                'columns': ('Автор', 'Кол-во рецептов'),
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
               'context': 'Список категорий',
               'columns': ('Наименование', 'Описание'),
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
                # message = f'Категория {title} сохранена'
                return redirect('/categories/show')
            else:
                message = f'Категория {title} уже существует'
        else:
            message = f'Не верные данные'
        logger.debug(message)
    else:
        form = CategoryForm()
        message = 'Заполните данные новой категории'
    context = {'form': form,
               'title': 'AddCategories', 'message': message,
               }

    return render(request, 'my_app/enter_param_form.html', context)


def show_recipes(request):
    recipes = Recipe.objects.all()
    context = {'title': 'Список рецептов',
               'context': 'Список рецептов',
               'columns': (
               'Наименование', 'Описание', 'Время приготовления', 'Опубликован', 'Создан', 'Изменить', 'Удалить'),
               'recipes': recipes
               }
    return render(request, 'my_app/show_recipes.html', context)


def add_recipes(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            cooking_steps = form.cleaned_data['cooking_steps']
            cooking_time = form.cleaned_data['cooking_time']
            image = form.cleaned_data['image']
            published = form.cleaned_data['published']
            if image is not None:
                fs = FileSystemStorage()
                fs.save(image.name, image)

            if request.user.is_authenticated:
                name_auth = request.user.username
                author = Author.objects.filter(name=name_auth).first()
                if author is None:
                    author = Author.objects.filter(pk=1).first()
            else:
                author = Author.objects.filter(pk=1).first()

            try:
                recipe = Recipe(category=Category.objects.filter(id=int(category)).first(),
                                title=title, description=description,
                                cooking_steps=cooking_steps, cooking_time=cooking_time,
                                author=author, published=published,
                                image=image)
                recipe.save()
                message = f'Рецепт {title} записан'
                logger.info(message)
                return redirect('/recipes/show')
            except IntegrityError as err:
                logger.warning(err)
                message = f'Наименование {title} уже существует'
            except Exception as err:
                logger.warning(err)
                message = 'Данные не сохранены'

        else:
            message = 'Неточные данные'
            logger.info(message)

    else:
        form = RecipeForm()
        message = 'Заполните данные'

    context = {'form': form,
               'title': 'AddRecipes',
               'message': message,
               }
    return render(request, 'my_app/add_recipe_form.html', context)


def find_recipe(request, recipe_pk: int):
    recipe = Recipe.objects.filter(pk=recipe_pk).first()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            cooking_steps = form.cleaned_data['cooking_steps']
            cooking_time = form.cleaned_data['cooking_time']
            image = form.cleaned_data['image']
            published = form.cleaned_data['published']
            # if image is not None:
            #     fs = FileSystemStorage()
            #     fs.save(image.name, image)

            try:
                Recipe.objects.filter(pk=recipe_pk).update(
                    title=title,
                    category=category,
                    description=description,
                    cooking_steps=cooking_steps,
                    cooking_time=cooking_time,
                    published=published,
                    # image=image,
                )
                message = f'Рецепт {title} обновлен'
                logger.info(message)
                return redirect('/recipes/show')
            except IntegrityError as err:
                logger.warning(err)
                message = f'Наименование {title} уже существует, или проблема изображения'
            except Exception as err:
                logger.warning(err)
                message = f'Данные не сохранены {err}'

        else:
            message = 'Не точные данные. Время приготовления должно иметь формат 00:00'
            logger.info(message)

    else:
        message = f'Изменение рецепта {recipe.title}'
        form = RecipeForm({'title': recipe.title,
                           'category': recipe.category.pk,
                           'description': recipe.description,
                           'cooking_steps': recipe.cooking_steps,
                           'cooking_time': recipe.cooking_time.strftime('%H:%M'),
                           'image': recipe.image,
                           'published': recipe.published,
                           })
    context = {'form': form,
               'message': message,
               'title': recipe.title,
               'recipe_pk': recipe_pk,
               'recipe': recipe,
               }

    return render(request, 'my_app/show_recipe_pk.html', context)


def delete_recipe(request, recipe_pk):
    recipe = Recipe.objects.filter(pk=recipe_pk).first()
    if request.method == 'POST':
        logger.info(f'Рецепт {recipe.title} удален')
        recipe.delete()
        return redirect('/recipes/show')

    form = RecipeForm()
    context = {'form': form,
               'message': f'Удалить рецепт {recipe.title} ?',
               'title': recipe.title,
               'recipe_pk': recipe_pk,
               }
    return render(request, 'my_app/delete_recipe_pk.html', context)


def show_items(request):
    items = Item.objects.all()
    context = {'title': 'Список номенклатуры',
               'context': 'Список ингридиентов',
               'columns': ('Наименование', 'Единица измерения'),
               'items': items
               }
    return render(request, 'my_app/show_items.html', context)


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            unit_measurement = form.cleaned_data['unit_measurement']
            try:
                item = Item(name=name, unit_measurement=unit_measurement)
                item.save()
                logger.info(f'Записано. item {name}')

                return redirect('/items_work/items/show')
            except IntegrityError as err:
                logger.warning(err)
                message = f'Наименование {name} уже существует'
            except Exception as err:
                logger.warning(err)
                message = 'Данные не сохранены'
        else:
            message = 'Неточные данные'
            logger.info(message)
    else:
        form = ItemForm()
        message = 'Добавление ингридиента'

    context = {'form': form,
               'title': 'AddItems',
               'message': message,
               }

    return render(request, 'my_app/enter_param_form.html', context)
