from rest_framework import serializers

from .models import Inventory, InventoryTransaction
from .services import MAX_QUANTITY


class CreateInventoryTransactionSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=InventoryTransaction.Type.choices)
    quantity = serializers.IntegerField(min_value=1, max_value=MAX_QUANTITY)
    reason = serializers.CharField(
        max_length=255, required=False, allow_blank=True, default=""
    )


class InventorySerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = ["product_id", "quantity", "updated_at"]
        read_only_fields = fields


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = [
            "id",
            "type",
            "quantity",
            "balance_before",
            "balance_after",
            "reason",
            "created_by",
            "created_at",
        ]
        read_only_fields = fields
