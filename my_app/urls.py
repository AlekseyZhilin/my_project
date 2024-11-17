from django.urls import path
from . views import index, show_authors, count_recipe_author, show_categories, add_category, show_recipes, add_recipes

urlpatterns = [
    path('', index, name='index'),
    path('authors/show', show_authors, name='show_authors'),
    path('authors/count_recipe', count_recipe_author, name='count_recipe_author'),
    path('categories/show', show_categories, name='show_categories'),
    path('categories/add', add_category, name='add_category'),
    path('recipes/show', show_recipes, name='Показать рецепты'),
    path('recipes/add', add_recipes, name='Добавить рецепт'),
]
