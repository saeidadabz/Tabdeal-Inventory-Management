from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

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

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def to_internal_value(self, data):

        data = data.copy()

        sku = data.get("sku")

        if isinstance(sku, str):
            data["sku"] = sku.strip().upper()

        return super().to_internal_value(data)

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Product name cannot be empty.")

        return value

    def validate_sku(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("SKU cannot be empty.")

        return value
