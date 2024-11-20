from django.core.management.base import BaseCommand
from my_app.models import Menu


class Command(BaseCommand):
    help = "Create menu"

    def handle(self, *args, **kwargs):
        menu_item = [Menu(name='Главная', url='/', position=1),
                     Menu(name='Авторы', url='/authors/show', position=2),
                     Menu(name='Категории', url='/categories/show', position=3),
                     Menu(name='Рецепты', url='/recipes/show', position=4),
                     Menu(name='Ингридиенты и работы', url='/items_work/items/show', position=5),
                     ]
        Menu.objects.bulk_create(menu_item)
        self.stdout.write(f'Пункты меню добавлены')
