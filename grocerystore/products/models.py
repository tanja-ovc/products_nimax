from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        'категория товара', max_length=70, unique=True, db_index=True)

    class Meta:
        verbose_name = 'категория товаров'
        verbose_name_plural = 'категории товаров'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(
        'название товара', max_length=70, unique=True, db_index=True)
    category = models.ManyToManyField(
        Category, verbose_name='категория', related_name='products',
        db_index=True)
    price = models.DecimalField(
        'цена', max_digits=8, decimal_places=2, validators=[
            MinValueValidator(
                Decimal('0.01'),
                'Цена товара должна быть положительным числом.')],
        db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name}'
