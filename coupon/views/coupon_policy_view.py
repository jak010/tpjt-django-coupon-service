from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from contrib.response import NormalResponse
from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateSchema, CouponPolicyListSchema
from coupon.services.coupon_policy_service import CouponPolicyService


class CouponPolicyView(APIView):

    @extend_schema(
        responses=CouponPolicyCreateSchema.CouponPolicyCreateResponse,
        request=CouponPolicyCreateSchema.CouponPolicyCreateRequest,
        summary="쿠폰 정책 생성하기"
    )
    def post(self, request):
        request_serializer = CouponPolicyCreateSchema.CouponPolicyCreateRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        new_coupon_policy = CouponPolicyService().create_coupon_policy(
            coupon_policy_command=request_serializer
        )

        return NormalResponse.success(
            CouponPolicyCreateSchema.CouponPolicyCreateResponse(
                {
                    "data": new_coupon_policy.to_dict()
                }
            )
        )

    @extend_schema(
        parameters=[CouponPolicyListSchema.CouponPolicyListRequest],
        responses=CouponPolicyListSchema.CouponPolicyListReponse,
        summary="쿠폰 정책 목록조회"
    )
    def get(self, request):
        request_serializer = CouponPolicyCreateSchema.CouponPolicyCreateRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        new_coupon_policy = CouponPolicyService().create_coupon_policy(
            coupon_policy_command=request_serializer
        )

        return NormalResponse.success(
            CouponPolicyCreateSchema.CouponPolicyCreateResponse(
                {
                    "data": new_coupon_policy.to_dict()
                }
            )
        )
