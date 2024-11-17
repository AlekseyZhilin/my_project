from django.core.management.base import BaseCommand
from my_app.models import Menu


class Command(BaseCommand):
    help = "Create menu"

    def handle(self, *args, **kwargs):
        menu_item = [Menu(name='Авторы', url='/authors/show', position=1),
                     Menu(name='Категории', url='/categories/show', position=2),
                     Menu(name='Рецепты', url='/recipes/show', position=3),
                     ]
        Menu.objects.bulk_create(menu_item)
        self.stdout.write(f'Пункты меню добавлены')
