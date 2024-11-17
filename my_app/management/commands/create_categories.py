from django.core.management.base import BaseCommand
from my_app.models import Category


class Command(BaseCommand):
    help = "Create categories"

    def handle(self, *args, **kwargs):
        categories = [Category(title='Первые блюда', description='Описание первых блюд'),
                      Category(title='Национальные блюда', description='Описание национальных блюд'),
                      ]
        Category.objects.bulk_create(categories)
        self.stdout.write(f'Категории добавлены')
