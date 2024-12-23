from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import CategoryForm, FindElement
from ..models import Category


def create_category(request):
    message = 'Создание категории'

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(show_categories)
        else:
            message = message + ' (не точные данные)'
    else:
        form = CategoryForm()

    content = {'form': form, 'title': 'Создание категории', 'message': message}
    return render(request, 'my_test/base_form.html', content)


def update_category(request, category_pk: int):
    message = 'Изменение категории'
    category = get_object_or_404(Category, pk=category_pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return redirect(show_categories)
            message = message + ' (нет изменений)'
        else:
            message = message + ' (не точные данные)'
    else:
        form = CategoryForm(instance=category)

    content = {'form': form, 'title': 'Изменение категории', 'message': message}
    return render(request, 'my_test/base_form.html', content)


def delete_category(request, category_pk: int):
    category = get_object_or_404(Category, pk=category_pk)

    if request.method == 'POST':
        try:
            category.delete()
            return redirect(show_categories)
        except ProtectedError as err:
            return HttpResponse(f'Не возможно удалить категорию {category}. Имеются ссылки')
    else:
        return render(request, 'my_test/delete_element.html', {'element': category})


def show_categories(request):
    search_text = None
    if request.method == 'POST':
        form = FindElement(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['element']

        if search_text is not None:
            categories = Category.objects.filter(name__icontains=search_text).order_by('name')
        else:
            categories = Category.objects.all().order_by('name')
    else:
        form = FindElement()
        categories = Category.objects.all().order_by('name')

    context = {'title': 'Категории',
               'columns': ('Наименование', 'Удалить'),
               'elements_table': categories,
               'find_form': form,
               }
    return render(request, 'my_test/show_categories.html', context)
