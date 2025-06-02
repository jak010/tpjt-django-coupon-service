from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from contrib.response import NormalResponse
from coupon.serializer.coupon_policy_serializer import (
    CouponPolicyCreateSchema
)
from coupon.services.v2.coupon_policy_service_v2 import CouponPolicyServiceV2


# HACK, 25.06.01 : Service Class는 DI로 해결하는게 ?


class V2CouponPolicyView(APIView):

    @extend_schema(
        operation_id="v2, 쿠폰 정책 생성하기",
        responses=CouponPolicyCreateSchema.CouponPolicyCreateResponse,
        request=CouponPolicyCreateSchema.CouponPolicyCreateRequest,
        summary="v2,쿠폰 정책 생성하기",
        tags=["v2, 쿠폰 정책"]
    )
    def post(self, request):
        request_serializer = CouponPolicyCreateSchema.CouponPolicyCreateRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        new_coupon_policy = CouponPolicyServiceV2().create_coupon_policy(
            request=request_serializer
        )


        return NormalResponse.success(
            CouponPolicyCreateSchema.CouponPolicyCreateResponse(
                {
                    "data": new_coupon_policy.to_dict()
                }
            )
        )