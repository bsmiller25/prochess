from django.core.management.base import BaseCommand, CommandError
from pcl.models import Division
from django.conf import settings


class Command(BaseCommand):
    help = 'Loads Divisions'
    def handle(self, *args, **options):
        divisions = ['Eastern', 'Central', 'Atlantic', 'Pacific']

        for div in divisions:
            print('Loading {}'.format(div))
            Division.objects.update_or_create(name=div)
