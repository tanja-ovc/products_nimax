# Generated by Django 4.2.4 on 2023-08-26 18:31

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=70, unique=True, verbose_name='категория товара')),
            ],
            options={
                'verbose_name': 'категория товаров',
                'verbose_name_plural': 'категории товаров',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=70, unique=True, verbose_name='название товара')),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'), 'Цена товара должна быть положительным числом.')], verbose_name='цена')),
                ('is_published', models.BooleanField(db_index=True, default=False)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('category', models.ManyToManyField(db_index=True, related_name='products', to='products.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
    ]
