from django.core.management.base import BaseCommand, CommandError
from ...models import Post, Category, PostCategory


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        d = 0
        for p1 in Post.objects.all():
            for c1 in p1.category.all():
                if c1.name == options['category']:
                    d += 1
        if d == 0:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {options["category"]}'))
