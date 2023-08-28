from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(lookup_expr='name__iexact')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ('category', 'price', 'is_published', 'is_deleted')
