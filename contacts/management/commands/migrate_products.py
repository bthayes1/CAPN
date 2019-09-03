from django.core.management.base import BaseCommand
from contacts.models import Product, Contact
from django.db import IntegrityError
import pandas as pd

class Command(BaseCommand):
    help = 'Import products into CAPN database'

    def add_arguments(self, parser):
        parser.add_argument('csvpath', nargs=1, type=str)

    def handle(self, *args, **options):
        sdf = pd.read_csv(options['csvpath'][0])

        for row in sdf.itertuples():
            self.stdout.write(row.catalog_number)
            support = Contact.objects.get(name=row.support)
            try:
                obj, created = Product.objects.update_or_create(
                    catalog_number = row.catalog_number,
                    defaults = {
                        'style_number':row.style_number,
                        'contact':support,
                    }
                )
            except IntegrityError:
                continue
            self.stdout.write(chr(27) + "[2J")

