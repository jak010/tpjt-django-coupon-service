from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from contrib.response import NormalResponse
from coupon.serializer.coupon_serializer import CouponCreateSchema, CouponSerializer
from coupon.services.coupon_service import CouponService


# HACK, 25.06.01 : Service Class는 DI로 해결하는게 ?


class CouponIssueView(APIView):

    @extend_schema(
        operation_id="쿠폰 생성하기",
        request=CouponCreateSchema.CouponCreateRequest,
        responses=CouponCreateSchema.CouponCreateResponse,
        summary="쿠폰 생성하기",
        tags=["쿠폰"]
    )
    def post(self, request):
        request_serializer = CouponCreateSchema.CouponCreateRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        new_coupon = CouponService().issue_coupon(
            request=request_serializer
        )

        return NormalResponse.success(
            CouponCreateSchema.CouponCreateResponse(
                {
                    "data": new_coupon.to_dict()
                }
            )
        )


class CouponUseView(APIView):

    @extend_schema(
        operation_id="쿠폰 사용하기",
        responses=CouponSerializer,
        request=None,
        summary="쿠폰 사용하기",
        tags=["쿠폰"]
    )
    def post(self, request, *args, **kwargs):
        coupon_id = kwargs.get("coupon_id")

        used_coupon = CouponService().use_coupon(
            coupon_id=coupon_id
        )

        return NormalResponse.success(
            CouponSerializer(used_coupon)
        )


class CouponCancelView(APIView):

    @extend_schema(
        responses=CouponSerializer,
        request=None,
        summary="쿠폰 취소",
        tags=["쿠폰"]
    )
    def delete(self, request, *args, **kwargs):
        coupon_id = kwargs.get("coupon_id")

        cancel_coupon = CouponService().cancel_coupon(coupon_id=coupon_id)

        return NormalResponse.success(
            CouponSerializer(cancel_coupon)
        )


class CouponDetailView(APIView):

    @extend_schema(
        operation_id="쿠폰 조회",
        responses=CouponSerializer,
        summary="쿠폰 조회",
        tags=["쿠폰"]
    )
    def get(self, *args, **kwargs):
        coupon_id = kwargs.get("coupon_id")

        coupon = CouponService().get_coupon(coupon_id=coupon_id)

        return NormalResponse.success(
            CouponSerializer(coupon)
        )
