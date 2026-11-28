from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from common.pagination import DefaultPagination
from common.serializers import ErrorResponseSerializer
from .models import Inventory, InventoryTransaction
from .serializers import (
    CreateInventoryTransactionSerializer,
    InventorySerializer,
    InventoryTransactionSerializer,
)
from .services import change_stock


class InventoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Inventory"],
        summary="Current stock of a product",
        responses={
            200: InventorySerializer,
            401: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    )
    def get(self, request, product_id):
        inventory = get_object_or_404(Inventory, product_id=product_id)
        return Response(InventorySerializer(inventory).data)


@extend_schema_view(
    get=extend_schema(
        tags=["Inventory"],
        summary="Stock change history (newest first)",
        responses={
            200: InventoryTransactionSerializer,
            401: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    ),
    post=extend_schema(
        tags=["Inventory"],
        summary="Record a stock change (IN = increase, OUT = decrease)",
        request=CreateInventoryTransactionSerializer,
        responses={
            201: InventoryTransactionSerializer,
            400: ErrorResponseSerializer,
            401: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
            409: ErrorResponseSerializer,
        },
    ),
)
class InventoryTransactionListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateInventoryTransactionSerializer
        return InventoryTransactionSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return InventoryTransaction.objects.none()
        inventory = get_object_or_404(Inventory, product_id=self.kwargs["product_id"])
        return inventory.transactions.all()  # Meta.ordering = ["-id"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        entry = change_stock(
            product_id=self.kwargs["product_id"],
            user=request.user,
            **serializer.validated_data,
        )
        return Response(
            InventoryTransactionSerializer(entry).data,
            status=status.HTTP_201_CREATED,
        )
