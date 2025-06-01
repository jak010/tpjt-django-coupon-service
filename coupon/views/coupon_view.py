from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from contrib.response import NormalResponse
from coupon.serializer.coupon_serializer import CouponCreateSchema, CouponSerializer
from coupon.services.coupon_service import CouponService


# HACK, 25.06.01 : Service Class는 DI로 해결하는게 ?


class CouponView(APIView):

    @extend_schema(
        request=CouponCreateSchema.CouponCreateRequest,
        responses=[CouponCreateSchema.CouponCreateResponse],
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
