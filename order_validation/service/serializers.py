from rest_framework import serializers


class ValidateOrderRequestSerializer(serializers.Serializer):

    id = serializers.CharField()
    account = serializers.CharField()
    portfolio = serializers.CharField()
    security = serializers.CharField()
    order_type = serializers.CharField()
    limit_price = serializers.DecimalField(required=False, max_digits=11, decimal_places=4)
    quantity = serializers.DecimalField(required=False, max_digits=11, decimal_places=4)
    price = serializers.DecimalField(required=False, max_digits=11, decimal_places=4)
    time_created = serializers.DateTimeField()
    time_approved = serializers.DateTimeField()

    class Meta:
        fields = (
            "id",
            "account",
            "portfolio",
            "security",
            "order_type",
            "limit_price",
            "quantity",
            "price",
            "time_created",
            "time_approved",
        )


class ValiateOrderResponseSerializer(serializers.Serializer):
    validation_status = serializers.CharField()
    reason = serializers.CharField()

    class Meta:
        fields = (
            "validation_status",
            "reason",
        )
