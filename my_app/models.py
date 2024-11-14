from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    age = models.PositiveSmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'author: {self.name}, age: {self.age}, email: {self.email}'


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'category: {self.title}'


class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    cooking_steps = models.TextField()
    cooking_time = models.TimeField()
    image = models.ImageField()
    authors = models.ManyToManyField(Author, related_name='recipes_authors')
    published = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'recipe: {self.title}, время: {self.cooking_time}, {short_text(self.cooking_steps.description)}'


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
