from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import MaterialsForm
from ..models import Materials, Specification


def add_row(request, spec_pk: int):
    message = 'Добавление строк'
    specification = Specification.objects.get(pk=spec_pk)
    materials = (specification.materials_table
                 .values('pk', 'item__name', 'count').all())

    if request.method == 'POST':
        form = MaterialsForm(request.POST)
        if form.is_valid():
            row = form.save()
            specification.materials_table.add(row)
            return redirect(add_row, spec_pk)
        else:
            message = message + ' (не точные данные)'
    else:
        form = MaterialsForm()

    content = {'form': form,
               'title': 'Добавление строк',
               'message': message,
               'columns': ('Номенклатура', 'Количество', 'Удалить'),
               'elements_table': materials,
               'spec_pk': spec_pk,
               }
    return render(request, 'my_test/materials_form.html', content)


def update_row(request, row_pk: int, spec_pk: int):
    message = 'Изменение строк'
    row = get_object_or_404(Materials, pk=row_pk)

    if request.method == 'POST':
        form = MaterialsForm(request.POST, instance=row)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return redirect(add_row, spec_pk)
            message = message + ' (нет изменений)'
        else:
            message = message + ' (не точные данные)'
    else:
        form = MaterialsForm(instance=row)

    content = {'form': form, 'title': 'Изменение строк', 'message': message}
    return render(request, 'my_test/base_form.html', content)


def delete_row(request, row_pk: int, spec_pk: int):
    row = get_object_or_404(Materials, pk=row_pk)

    if request.method == 'POST':
        row.delete()
        return redirect(add_row, spec_pk)
    else:
        return render(request, 'my_test/delete_element.html', {'element': row})
