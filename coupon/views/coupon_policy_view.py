from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from contrib.response import NormalResponse
from coupon.serializer.coupon_policy_serializer import (
    CouponPolicyCreateSchema,
    CouponPolicyListSchema,
    CouponPolicyModel
)
from coupon.services.coupon_policy_service import CouponPolicyService


# HACK, 25.06.01 : Service Class는 DI로 해결하는게 ?


class CouponPolicyView(APIView):

    @extend_schema(
        responses=CouponPolicyCreateSchema.CouponPolicyCreateResponse,
        request=CouponPolicyCreateSchema.CouponPolicyCreateRequest,
        summary="쿠폰 정책 생성하기",
        tags=["쿠폰 정책"]
    )
    def post(self, request):
        request_serializer = CouponPolicyCreateSchema.CouponPolicyCreateRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        new_coupon_policy = CouponPolicyService().create_coupon_policy(
            request=request_serializer
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
        responses=CouponPolicyListSchema.CouponPolicyPaginateListReponse,
        summary="쿠폰 정책 목록조회",
        tags=["쿠폰 정책"]
    )
    def get(self, request):
        request_serializer = CouponPolicyListSchema.CouponPolicyListRequest(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)

        coupon_polices = CouponPolicyService().get_all_coupon_policy(request=request_serializer)

        return NormalResponse.page(
            CouponPolicyListSchema.CouponPolicyPaginateListReponse(
                data=coupon_polices.to_dict()
            )
        )


class CouponPolicyDetailView(APIView):
    @extend_schema(
        responses=CouponPolicyModel,
        summary="쿠폰 정책 목록조회",
        tags=["쿠폰 정책"]
    )
    def get(self, *args, **kwargs):
        coupon_policy = CouponPolicyService().get_coupon_policy(
            coupon_policy_id=kwargs.get("coupon_policy_id")
        )

        if coupon_policy is None:
            raise NotFound()  # Hack, 25.06.01 : 데이터 형식 맞추기

        return NormalResponse.page(
            CouponPolicyModel(
                data=coupon_policy.to_dict()
            )
        )
