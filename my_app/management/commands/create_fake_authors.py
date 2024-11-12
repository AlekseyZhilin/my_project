from django.core.management.base import BaseCommand
from my_app.models import Author


class Command(BaseCommand):
    help = "Create fake user"

    def add_arguments(self, parser):
        parser.add_argument('count_authors', type=int, help='count author')

    def handle(self, *args, **kwargs):
        count_authors = kwargs['count_authors']
        for i in range(1, count_authors + 1):
            author = Author(name=f'name{i}', email=f'test{i}@mail.ru', age=25 + i)
            author.save()

        self.stdout.write(f'create {count_authors} authors')
