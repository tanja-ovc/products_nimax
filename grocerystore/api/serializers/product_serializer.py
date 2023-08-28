from rest_framework import serializers

from api.serializers import CategorySerializer
from products.models import Category, Product


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'is_published',
                  'is_deleted')


class CategoryReprField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
        }


class ProductWriteSerializer(serializers.ModelSerializer):

    category = CategoryReprField(
        queryset=Category.objects.all(), slug_field='name', many=True)

    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'is_published', 'is_deleted')

    def validate_category(self, value):
        if len(value) < 2 or len(value) > 10:
            raise serializers.ValidationError(
                'Товар нужно отнести как минимум к двум категориям, '
                'но не более, чем к десяти категориям.'
            )
        return value
