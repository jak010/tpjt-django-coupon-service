from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from contrib.response import NormalResponse
from coupon.serializer.coupon_policy_serializer import (
    CouponPolicyCreateSchema, CouponPolicyModel, CouponPolicyListSchema
)
from coupon.services.v2.coupon_policy_service_v2 import CouponPolicyServiceV2


# HACK, 25.06.01 : Service Class는 DI로 해결하는게 ?


class V2CouponPolicyView(APIView):

    @extend_schema(
        operation_id="v2, 쿠폰 정책",
        responses=CouponPolicyListSchema.CouponPolicyListResponse,
        request=None,
        summary="v2,쿠폰 정책 목록조회",
        tags=["v2, 쿠폰 정책"]
    )
    def get(self, request):
        all_coupon_policy = CouponPolicyServiceV2().get_all_coupon_policy()

        return NormalResponse.success(
            CouponPolicyListSchema.CouponPolicyListResponse(
                {
                    "items": all_coupon_policy
                }
            )
        )

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


class V2CouponPolicyDetailView(APIView):

    @extend_schema(
        operation_id="v2, 쿠폰 정책 조회하기",
        responses=CouponPolicyCreateSchema.CouponPolicyCreateResponse,
        request=CouponPolicyCreateSchema.CouponPolicyCreateRequest,
        summary="v2,쿠폰 정책 조회하기",
        tags=["v2, 쿠폰 정책"]
    )
    def get(self, *args, **kwargs):
        coupon_policy = CouponPolicyServiceV2().get_coupon_policy(
            coupon_policy_id=kwargs.get("coupon_policy_id")
        )

        return NormalResponse.success(
            CouponPolicyModel(coupon_policy)
        )
