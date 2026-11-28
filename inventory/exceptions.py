from rest_framework import status

from common.exceptions import DomainError


class InvalidQuantity(DomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Quantity must be a positive integer."
    default_code = "invalid_quantity"


class ProductNotFound(DomainError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Product not found."
    default_code = "product_not_found"


class ProductInactive(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Inventory of an inactive product cannot be changed."
    default_code = "product_inactive"


class InsufficientStock(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Insufficient stock."
    default_code = "insufficient_stock"
