from django import forms
from django.forms import TextInput

from .models import Specification, Items, Category, Materials


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'unit_measurement', 'category', 'is_product')
        labels = {'name': 'Наименование',
                  'unit_measurement': 'Единицы измерения',
                  'category': 'Категория',
                  'is_product': 'Это продукция',
                  }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {'name': 'Наименование'}
        # help_texts = {'name': 'Введите наименование'}


class SpecificationForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Items.objects.filter(is_product=True), label='Продукция')

    class Meta:
        model = Specification
        fields = ('product', 'category',)
        labels = {'product': 'Продукция',
                  'category': 'Категория',
                  }

    def get_pk(self):
        return self.instance.pk


class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ('item', 'count',)
        labels = {'item': 'Номенклатура', 'count': 'Количество'}
        widgets = {'count': TextInput(attrs={'size': 8})}


class FindElement(forms.Form):
    element = forms.CharField(max_length=50, required=False, label='Найти')
