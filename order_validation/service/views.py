from rest_framework import generics, status
from rest_framework.views import Response


from service.securities import SECURITIES
from service.serializers import ValidateOrderRequestSerializer, ValiateOrderResponseSerializer
from service.types import OrderType, ValidationStatus


class ValidateOrderView(generics.GenericAPIView):
    def post(self, request):
        resp_status, resp = self.validate_order(request.data)
        return Response(status=resp_status, data=resp.validated_data)


def validate_order(order_data):
    serializer = ValidateOrderRequestSerializer(data=order_data)
    serializer.is_valid(raise_exception=True)

    security = serializer.validated_data["security"]
    order_type = serializer.validated_data["order_type"]
    limit_price = serializer.validated_data.get("limit_price")
    quantity = serializer.validated_data.get("quantity")
    price = serializer.validated_data.get("price")

    if security not in SECURITIES:
        resp_status = status.HTTP_400_BAD_REQUEST
        resp = ValiateOrderResponseSerializer(data={
            "validation_status": ValidationStatus.INVALID.name,
            "reason": "Invalid security provided.",
        })
    elif order_type not in [OrderType.MARKET.name, OrderType.LIMIT.name]:
        resp_status = status.HTTP_400_BAD_REQUEST
        resp = ValiateOrderResponseSerializer(data={
            "validation_status": ValidationStatus.INVALID.name,
            "reason": "Invalid order type provided. Must be either MARKET or LIMIT.",
        })
    elif order_type == OrderType.MARKET.name and limit_price is not None:
        resp_status = status.HTTP_400_BAD_REQUEST
        resp = ValiateOrderResponseSerializer(data={
            "validation_status": ValidationStatus.BORDERLINE.name,
            "reason": "Market order placed with limit price provided.",
        })
    elif order_type == OrderType.LIMIT.name and limit_price is None:
        resp_status = status.HTTP_400_BAD_REQUEST
        resp = ValiateOrderResponseSerializer(data={
            "validation_status": ValidationStatus.INVALID.name,
            "reason": "Limit order placed with no limit price provided.",
        })
    elif price is None == quantity is None:
        # Exactly one of price or quantity should be provided.
        resp_status = status.HTTP_400_BAD_REQUEST
        resp = ValiateOrderResponseSerializer(data={
            "validation_status": ValidationStatus.INVALID.name,
            "reason": "Exactly one of price or quantity should be provided.",
        })
    else:
        resp_status = status.HTTP_200_OK
        resp = ValiateOrderResponseSerializer(data={
            "validation_status": ValidationStatus.VALID.name,
            "reason": "Order validation successful.",
        })

    resp.is_valid(raise_exception=True)

    return resp_status, resp
