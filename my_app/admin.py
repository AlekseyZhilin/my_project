from django.contrib import admin
from . models import Author, Category, Recipe, Menu, Item, Specification


@admin.action(description="Опубликовать рецепты")
def published_recipe(modeladmin, request, queryset):
    queryset.update(published=True)


@admin.action(description="Отменить публикацию рецептов")
def un_published_recipe(modeladmin, request, queryset):
    queryset.update(published=False)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'cooking_time', 'published', 'author']
    list_filter = ['created_date', 'category']
    search_fields = ['title']
    actions = [published_recipe, un_published_recipe]


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name']


class SpecificationAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Menu)
