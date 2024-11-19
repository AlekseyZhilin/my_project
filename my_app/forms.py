from django import forms
from . models import Category


class SelectPramForm(forms.Form):
    count_recipe = forms.IntegerField(min_value=0, label='Количество рецептов автора')


class CategoryForm(forms.Form):
    title = forms.CharField(max_length=100, label='Наименование')
    description = forms.CharField(label='Описание', required=False)


class RecipeForm(forms.Form):
    category = forms.ChoiceField(
        choices=[(item['id'], item['title']) for item in Category.objects.values('id', 'title').all()],
        label='Категория'
    )
    title = forms.CharField(max_length=100, label='Наименование')
    description = forms.CharField(label='Описание', required=False)
    cooking_steps = forms.CharField()
    cooking_time = forms.TimeField(input_formats=['%H:%M'], initial='00:00', label='Время приготовления')
    image = forms.ImageField(label='Изображение', required=False)
    published = forms.BooleanField(label='Опубликовать', required=False)
