from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import ItemForm, FindElement
from ..models import Items


def create_item(request):
    message = 'Создание номенклатуры'

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(show_items)
        else:
            message = message + ' (не точные данные)'
    else:
        form = ItemForm()

    content = {'form': form, 'title': 'Создание номенклатуры', 'message': message}
    return render(request, 'my_test/base_form.html', content)


def update_item(request, item_pk: int):
    message = 'Изменение номенклатуры'
    item = get_object_or_404(Items, pk=item_pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return redirect(show_items)
            message = message + ' (нет изменений)'
        else:
            message = message + ' (не точные данные)'
    else:
        form = ItemForm(instance=item)

    content = {'form': form, 'title': 'Изменение номенклатуры', 'message': message}
    return render(request, 'my_test/base_form.html', content)


def delete_item(request, item_pk: int):
    item = get_object_or_404(Items, pk=item_pk)

    if request.method == 'POST':
        try:
            item.delete()
            return redirect(show_items)
        except ProtectedError as err:
            return HttpResponse(f'Не возможно удалить номенклатуру {item}. Имеются ссылки')
    else:
        return render(request, 'my_test/delete_element.html', {'element': item})


def show_items(request):
    search_text = None
    if request.method == 'POST':
        form = FindElement(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['element']

        if search_text is not None:
            items = (Items.objects
                     .values('pk', 'name', 'unit_measurement', 'is_product', 'category__name')
                     .filter(name__icontains=search_text).order_by('name'))
        else:
            items = None
    else:
        form = FindElement()
        items = (Items.objects
                 .values('pk', 'name', 'unit_measurement', 'is_product', 'category__name')
                 .all().order_by('name'))

    context = {'title': 'Номенклатура',
               'columns': ('Наименование', 'Единицы измерения', 'Категория', 'Продукция', 'Удалить'),
               'elements_table': items,
               'find_form': form,
               }
    return render(request, 'my_test/show_items.html', context)
