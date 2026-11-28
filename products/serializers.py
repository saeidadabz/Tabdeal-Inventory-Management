from rest_framework import serializers

from .models import Product


class SKUField(serializers.CharField):
    """Trim (by CharField) + uppercase, before any validator runs."""

    def to_internal_value(self, data):
        return super().to_internal_value(data).upper()


class ProductSerializer(serializers.ModelSerializer):
    sku = SKUField(max_length=64)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
