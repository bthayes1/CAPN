from django.core.management.base import BaseCommand
from contacts.models import Contact
import pandas as pd

class Command(BaseCommand):
    help = 'Import contacts into CAPN database'

    def add_arguments(self, parser):
        parser.add_argument('csvpath', nargs=1, type=str)

    def handle(self, *args, **options):
        sdf = pd.read_csv(options['csvpath'][0])

        for row in sdf.itertuples():
            self.stdout.write(row.support)
            obj, created = Contact.objects.update_or_create(
                name = row.support,
                defaults = {
                    'phone':row.phone,
                    'email':row.email,
                    'link':row.page,
                }
            )
