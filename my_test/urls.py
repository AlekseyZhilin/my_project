from django.urls import path
from . views import index
from . views_.categories import create_category, update_category, delete_category, show_categories
from .views_.items import create_item, update_item, delete_item, show_items
from .views_.specifications import create_specification, update_specification, delete_specification, show_specifications
from .views_.materials import add_row, update_row, delete_row

urlpatterns = [
    path('', index, name='index'),
    path('items/create_item', create_item, name='create_item'),
    path('items/update_item/<int:item_pk>/', update_item, name='update_item'),
    path('items/delete_item/<int:item_pk>/', delete_item, name='delete_item'),
    path('items/show_items', show_items, name='show_items'),

    path('cat/create_cat', create_category, name='create_category'),
    path('cat/update_cat/<int:category_pk>/', update_category, name='update_category'),
    path('cat/delete_cat/<int:category_pk>/', delete_category, name='delete_category'),
    path('cat/show_cats', show_categories, name='show_categories'),

    path('spec/create_spec', create_specification, name='create_specification'),
    path('spec/update_spec/<int:spec_pk>/', update_specification, name='update_specification'),
    path('spec/delete_spec/<int:spec_pk>/', delete_specification, name='delete_specification'),
    path('spec/show_spec', show_specifications, name='show_specifications'),

    path('table/add_row/<int:spec_pk>/', add_row, name='add_row'),
    path('table/update_row/<int:row_pk>/<int:spec_pk>/', update_row, name='update_row'),
    path('table/delete_row/<int:row_pk>/<int:spec_pk>/', delete_row, name='delete_row'),
]
