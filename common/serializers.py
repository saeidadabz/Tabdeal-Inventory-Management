from rest_framework import serializers


class ErrorBodySerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()
    details = serializers.JSONField(allow_null=True)


class ErrorResponseSerializer(serializers.Serializer):
    """Only used to document error responses in Swagger (drf-spectacular)."""

    error = ErrorBodySerializer()
