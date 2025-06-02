from rest_framework import serializers

from coupon.models.coupon import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class CouponCreateSchema(serializers.Serializer):
    class CouponCreateRequest(serializers.Serializer):
        coupon_policy_id = serializers.IntegerField()

    class CouponCreateResponse(serializers.Serializer):
        data = CouponSerializer()


class CouponUseSchema(serializers.Serializer):
    class CouponUseRequest(serializers.Serializer):
        coupon_id = serializers.IntegerField()

    class CouponUseResponse(serializers.Serializer):
        data = CouponSerializer()
