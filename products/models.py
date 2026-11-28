from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["name"],
                name="product_name_idx",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"
