from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from api.filters import ProductFilter
from api.serializers import ProductReadSerializer, ProductWriteSerializer
from products.models import Product


class ProductViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ('name',)
    ordering_fields = ('id',)
    ordering = ('id',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ProductWriteSerializer
        return ProductReadSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        message = {'Товар удалён': 'Товар отмечен как удалённый.'}
        return Response(message, status=status.HTTP_200_OK)
