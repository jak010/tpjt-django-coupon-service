from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from contrib.response import NormalResponse
from coupon.exceptions.coupon import NotEnoughCoupon
from coupon.serializer.coupon_serializer import CouponCreateSchema
from coupon.services.v2.coupon_service_v2 import CouponServiceV2
from coupon.services.v1.coupon_service import CouponRDBService


class V2CouponIssueView(APIView):
    coupon_service = CouponServiceV2()
    
    @extend_schema(
        operation_id="쿠폰 생성하기",
        request=CouponCreateSchema.CouponCreateRequest,
        responses=CouponCreateSchema.CouponCreateResponse,
        summary="쿠폰 생성하기",
        tags=["v2,쿠폰"]
    )
    def post(self, request):
        request_serializer = CouponCreateSchema.CouponCreateRequest(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        try:
            new_coupon = self.coupon_service.issue_coupon(
                request=request_serializer
            )
        except NotEnoughCoupon as e:
            return NormalResponse.failure(desc=str(e.default_detail))

        return NormalResponse.success(
            CouponCreateSchema.CouponCreateResponse(
                {
                    "data": new_coupon
                }
            )
        )
