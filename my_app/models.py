import datetime

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(default='', blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.name}, age: {self.age}, email: {self.email}'


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='', blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.title}'


class Work(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name


UNIT_MEASURE = (('кг', 'кг'), ('гр', 'гр'), ('шт', 'шт'), ('л', 'л'), ('мл', 'мл'))


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit_measurement = models.CharField(max_length=20, default=UNIT_MEASURE[0][0])
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.name}, {self.unit_measurement}'


class Specification(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    item = models.ForeignKey(Item, on_delete=models.SET_DEFAULT, related_name='items', default=None)
    count = models.DecimalField(max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=' ', blank=True)
    cooking_steps = models.CharField(max_length=200, default='')
    cooking_time = models.TimeField()
    image = models.ImageField(default='', blank=True, null=True, upload_to='img')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='authors', default=None, null=True)
    published = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.title}, время: {self.cooking_time}'


class Menu(models.Model):
    name = models.CharField('Название', max_length=100)
    url = models.CharField('Ссылка', max_length=100)
    position = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'


def short_text(text):
    if len(text) > 5:
        return str([word for word in text.split()[:5]]) + '...'

    return text
