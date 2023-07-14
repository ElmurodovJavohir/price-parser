from django.core.management.base import BaseCommand, CommandError
from tablib import Dataset

from product.models import Product
from product.resources import ProductResource


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        person_resource = ProductResource()
        dataset = Dataset()
        new_persons = open("product.csv", "r", encoding="utf-8", newline="")

        imported_data = dataset.load(new_persons.read(), format="csv")
        # print(dataset)
        # print(imported_data)
        result = person_resource.import_data(
            dataset, dry_run=True, raise_errors=True
        )  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now
        else:
            print(result.row_errors())
            print("erroooorr")
