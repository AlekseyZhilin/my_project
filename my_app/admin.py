from django.contrib import admin
from . models import Author, Category, Recipe, Menu

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Menu)
