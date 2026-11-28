from django.db import transaction

from .exceptions import (
    InsufficientStock,
    InvalidQuantity,
    ProductInactive,
    ProductNotFound,
)
from .models import Inventory, InventoryTransaction

MAX_QUANTITY = 1_000_000_000  # per operation (documented simplification)


def _validate_quantity(quantity) -> None:
    # bool is a subclass of int, so it must be rejected explicitly
    if (
        not isinstance(quantity, int)
        or isinstance(quantity, bool)
        or not (1 <= quantity <= MAX_QUANTITY)
    ):
        raise InvalidQuantity(details={"min": 1, "max": MAX_QUANTITY})


def change_stock(
    *,
    product_id: int,
    type: str,
    quantity: int,
    reason: str = "",
    user=None,
) -> InventoryTransaction:
    """
    The ONLY place where stock changes.

    Everything happens in one DB transaction: either the balance AND the
    ledger entry are both written, or nothing is.
    """
    if type not in InventoryTransaction.Type.values:
        raise ValueError(f"Unknown transaction type: {type!r}")  # programmer error
    _validate_quantity(quantity)

    with transaction.atomic():
        # Row lock: concurrent changes on the same product wait here, one by one.
        try:
            inventory = (
                Inventory.objects.select_for_update(of=("self",))
                .select_related("product")
                .get(product_id=product_id)
            )
        except Inventory.DoesNotExist:
            raise ProductNotFound() from None

        if not inventory.product.is_active:
            raise ProductInactive()

        before = inventory.quantity
        if type == InventoryTransaction.Type.IN:
            after = before + quantity
        else:
            if quantity > before:
                raise InsufficientStock(
                    details={"available": before, "requested": quantity}
                )
            after = before - quantity

        inventory.quantity = after
        inventory.save(update_fields=["quantity", "updated_at"])

        return InventoryTransaction.objects.create(
            inventory=inventory,
            type=type,
            quantity=quantity,
            balance_before=before,
            balance_after=after,
            reason=reason,
            created_by=user,
        )


def increase_stock(**kwargs) -> InventoryTransaction:
    return change_stock(type=InventoryTransaction.Type.IN, **kwargs)


def decrease_stock(**kwargs) -> InventoryTransaction:
    return change_stock(type=InventoryTransaction.Type.OUT, **kwargs)
