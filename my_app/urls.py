from django.urls import path
from . views import (index,
                     show_authors, count_recipe_author,
                     show_categories, add_category,
                     show_recipes, add_recipes, find_recipe, delete_recipe,
                     show_items, add_item
                     )

urlpatterns = [
    path('', index, name='index'),
    path('authors/show', show_authors, name='show_authors'),
    path('authors/count_recipe', count_recipe_author, name='count_recipe_author'),
    path('categories/show', show_categories, name='show_categories'),
    path('categories/add', add_category, name='add_category'),
    path('recipes/show', show_recipes, name='show_recipes'),
    path('recipes/add', add_recipes, name='add_recipes'),
    path('recipes/find/<int:recipe_pk>/', find_recipe, name='find_recipe'),
    path('recipes/delete/<int:recipe_pk>/', delete_recipe, name='delete_recipe'),
    path('items_work/items/show', show_items, name='show_items'),
    path('items_work/items/add', add_item, name='add_item'),
]
