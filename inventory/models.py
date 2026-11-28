from django.conf import settings
from django.db import models
from django.db.models import F, Q


class Inventory(models.Model):
    product = models.OneToOneField(
        "products.Product", on_delete=models.PROTECT, related_name="inventory"
    )
    quantity = models.PositiveBigIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventories"
        constraints = [
            # last line of defense: even buggy code can't persist a negative balance
            models.CheckConstraint(
                condition=Q(quantity__gte=0), name="inventory_quantity_gte_0"
            ),
        ]

    def __str__(self):
        return f"Inventory(product={self.product_id}, qty={self.quantity})"


class InventoryTransaction(models.Model):
    """Append-only ledger entry. Never updated, never deleted."""

    class Type(models.TextChoices):
        IN = "IN", "Increase"
        OUT = "OUT", "Decrease"

    inventory = models.ForeignKey(
        Inventory, on_delete=models.PROTECT, related_name="transactions"
    )
    type = models.CharField(max_length=3, choices=Type.choices)
    quantity = (
        models.PositiveBigIntegerField()
    )  # always positive; direction comes from `type`
    balance_before = models.PositiveBigIntegerField()
    balance_after = models.PositiveBigIntegerField()
    reason = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_transactions"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["inventory", "-id"], name="invtx_inventory_id_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0), name="invtx_quantity_gt_0"
            ),
            # the ledger arithmetic must always add up
            models.CheckConstraint(
                condition=(
                    Q(type="IN", balance_after=F("balance_before") + F("quantity"))
                    | Q(type="OUT", balance_before=F("balance_after") + F("quantity"))
                ),
                name="invtx_balance_consistent",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise RuntimeError("InventoryTransaction is append-only.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise RuntimeError("InventoryTransaction is append-only.")
