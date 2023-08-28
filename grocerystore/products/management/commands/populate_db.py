import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from products.models import Category, Product

MODEL_NAME_FILE = {
    'category': (Category, 'category.csv'),
    'product': (Product, 'product.csv'),
}


class Command(BaseCommand):
    help = 'Load data from a csv file to the corresponding db table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_csv_file(filename):
        return os.path.join(
            settings.BASE_DIR, 'products', 'csv_data', filename
        )

    @staticmethod
    def clear_model(model):
        model.objects.all().delete()

    def print_to_terminal(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def load_model(self, model_name, field_names):
        model, file_path = MODEL_NAME_FILE.get(model_name)
        with open(self.get_csv_file(file_path)) as file:
            reader = csv.reader(file, delimiter=',')
            self.clear_model(model)
            line = 0
            for row in reader:
                if row != '' and line > 0:
                    params = dict(zip(field_names, row))
                    _, created = model.objects.get_or_create(**params)
                line += 1
        self.print_to_terminal(
            f'{line - 1} objects added to "{model_name}" table'
        )

    def connecting_related_models(self,
                                  main_model,
                                  related_model,
                                  relational_field,
                                  through_model_name):

        with open(self.get_csv_file(f'_{through_model_name}.csv')) as file:
            reader = csv.reader(file, delimiter=',')
            line = 0
            for row in reader:
                if row != '' and line > 0:
                    main_object = get_object_or_404(
                        main_model, pk=row[1])
                    related_object = get_object_or_404(
                        related_model, pk=row[2])
                    main_obj_attr = getattr(main_object, relational_field)
                    main_obj_attr.add(related_object)
                line += 1
        self.print_to_terminal(
            f'{line - 1} objects added to intermediate table '
            f'"{through_model_name}"'
        )

    def load_category(self):
        self.load_model(
            'category',
            ('id', 'name')
        )

    def load_product(self):
        self.load_model(
            'product',
            ('id', 'name', 'price')
        )
        self.connecting_related_models(
            Product, Category,
            relational_field='category',
            through_model_name='product_category')

    def handle(self, *args, **kwargs):
        self.load_category()
        self.load_product()
