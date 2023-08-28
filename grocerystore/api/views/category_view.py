from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.serializers import CategorySerializer
from products.models import Category


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.products.first():
            error = {'Ошибка': 'Категорию нельзя удалить, пока к ней '
                     'отнесены товары.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
