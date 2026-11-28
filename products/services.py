from django.db import transaction

from .models import Product


@transaction.atomic
def create_product(
    *,
    name: str,
    sku: str,
    description: str = "",
    is_active: bool = True,
) -> Product:
    """
    Create a product.

    Business operations related to product creation
    should be orchestrated here.
    """

    product = Product.objects.create(
        name=name,
        sku=sku,
        description=description,
        is_active=is_active,
    )

    return product
