from django.urls import path

from . import views

urlpatterns = [
    path(
        "products/<int:product_id>/inventory/",
        views.InventoryDetailView.as_view(),
        name="inventory-detail",
    ),
    path(
        "products/<int:product_id>/inventory/transactions/",
        views.InventoryTransactionListCreateView.as_view(),
        name="inventory-transactions",
    ),
]
