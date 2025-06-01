from rest_framework import serializers

from coupon.models.coupon_policy import CouponPolicy
from coupon.models.coupon import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class CouponCreateSchema(serializers.Serializer):
    class CouponCreateRequest(serializers.Serializer):
        coupon_policy_id = serializers.IntegerField()
