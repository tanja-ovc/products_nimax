from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'is_published', 'is_deleted')

    def clean(self):
        categories = self.cleaned_data.get('category')
        if categories.count() < 2 or categories.count() > 10:
            raise ValidationError(
                'Товар нужно отнести как минимум к двум категориям, '
                'но не более, чем к десяти категориям.')
        return self.cleaned_data


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'is_published', 'is_deleted')
