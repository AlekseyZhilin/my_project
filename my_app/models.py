from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    age = models.PositiveSmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.name}, age: {self.age}, email: {self.email}'


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
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


UNIT_MEASURE = (('кг', 'кг'), ('шт', 'шт'), ('л', 'л'))


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit_measurement = models.CharField(max_length=20, default=UNIT_MEASURE[0][0])
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.name}, {self.unit_measurement}'


class Operation(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='works')
    position = models.PositiveSmallIntegerField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.position}. {self.work.name}, {self.time}'


class Specification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')
    count = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.operation} {self.item.name}, {self.count}'


class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=' ', blank=True)
    cooking_steps = models.CharField(max_length=200, default='')
    cooking_time = models.TimeField()
    #items = models.ForeignKey(Specification, on_delete=models.CASCADE, related_name='specification_recipes', null=True, default=None)
    image = models.ImageField(default='', blank=True)
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
