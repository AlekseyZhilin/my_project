from django import forms
from . models import Category, UNIT_MEASURE


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    email = forms.EmailField()
    age = forms.IntegerField(label='Возраст')
    description = forms.CharField(max_length=100, label='О себе', required=False, widget=forms.Textarea)


class SelectPramForm(forms.Form):
    count_recipe = forms.IntegerField(min_value=0, label='Количество рецептов автора')


class CategoryForm(forms.Form):
    title = forms.CharField(max_length=100, label='Наименование')
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea)


class RecipeForm(forms.Form):
    category = forms.ChoiceField(
        choices=[(item['id'], item['title']) for item in Category.objects.values('id', 'title').all()],
        label='Категория'
    )
    title = forms.CharField(max_length=100, label='Наименование')
    description = forms.CharField(label='Описание', required=False)
    cooking_steps = forms.CharField(widget=forms.Textarea, label='Шаги приготовления')
    cooking_time = forms.TimeField(input_formats=['%H:%M'], initial='00:00', label='Время приготовления')
    image = forms.ImageField(label='Изображение', required=False)
    published = forms.BooleanField(label='Опубликовать', required=False)


class ItemForm(forms.Form):
    name = forms.CharField(max_length=100, label='Наименование')
    unit_measurement = forms.ChoiceField(choices=UNIT_MEASURE, label='Единица измерения')


class WorkForm(forms.Form):
    name = forms.CharField(max_length=100, label='Наименование')
