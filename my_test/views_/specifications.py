from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import SpecificationForm, FindElement
from ..models import Specification


def create_specification(request):
    message = 'Создание спецификации'

    if request.method == 'POST':
        form = SpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(update_specification, form.get_pk())
        else:
            message = message + ' (не точные данные)'
    else:
        form = SpecificationForm()

    content = {'form': form, 'title': 'Создание спецификации', 'message': message}
    return render(request, 'my_test/base_form.html', content)


def update_specification(request, spec_pk: int):
    message = 'Изменение спецификации'
    specification = get_object_or_404(Specification, pk=spec_pk)
    count_materials = specification.materials_table.count()

    if request.method == 'POST':
        form = SpecificationForm(request.POST, instance=specification)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return redirect(show_specifications)
            message = message + ' (нет изменений)'
        else:
            message = message + ' (не точные данные)'
    else:
        form = SpecificationForm(instance=specification)

    content = {'form': form,
               'title': 'Изменение спецификации',
               'message': message,
               'spec_pk': specification.pk,
               'count_materials': count_materials,
               }
    return render(request, 'my_test/spec_form.html', content)


def delete_specification(request, spec_pk: int):
    specification = get_object_or_404(Specification, pk=spec_pk)

    if request.method == 'POST':
        try:
            specification.delete()
            return redirect(show_specifications)
        except ProtectedError as err:
            return HttpResponse(f'Не возможно удалить спецификацию {specification}. Имеются ссылки')
    else:
        return render(request, 'my_test/delete_element.html', {'element': specification})


def show_specifications(request):
    search_text = None
    if request.method == 'POST':
        form = FindElement(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['element']

        if search_text is not None:
            specifications = (Specification.objects
                              .values('pk', 'category__name', 'product__name')
                              .filter(product__name__icontains=search_text).order_by('product__name'))
        else:
            specifications = None
    else:
        form = FindElement()
        specifications = (Specification.objects
                          .values('pk', 'category__name', 'product__name')
                          .all().order_by('product__name'))

    context = {'title': 'Спецификации',
               'columns': ('Продукция', 'Категория', 'Удалить'),
               'elements_table': specifications,
               'find_form': form,
               }
    return render(request, 'my_test/show_specifications.html', context)
