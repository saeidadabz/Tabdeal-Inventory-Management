from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Product
from .serializers import ProductSerializer
from .services import create_product


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(tags=["Products"], summary="List products"),
    retrieve=extend_schema(tags=["Products"], summary="Get a product"),
    create=extend_schema(tags=["Products"], summary="Create a product"),
    update=extend_schema(tags=["Products"], summary="Replace a product"),
    partial_update=extend_schema(tags=["Products"], summary="Update a product"),
    destroy=extend_schema(tags=["Products"], summary="Delete a product"),
)
class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticated]

    pagination_class = ProductPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "name",
        "sku",
        "description",
    ]

    ordering_fields = [
        "name",
        "sku",
        "created_at",
        "updated_at",
    ]

    ordering = ["-created_at"]

    # http_method_names = [
    #     "get",
    #     "post",
    #     "put",
    #     "patch",
    #     "head",
    #     "options",
    # ]

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        product = create_product(**serializer.validated_data)

        serializer.instance = product
