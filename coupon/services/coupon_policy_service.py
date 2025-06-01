from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction

from coupon.models.coupon_policy import CouponPolicy

if TYPE_CHECKING:
    from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateSchema


class CouponPolicyService:

    @transaction.atomic
    def create_coupon_policy(self,
                             request: CouponPolicyCreateSchema.CouponPolicyCreateRequest
                             ):
        """ 쿠폰 정책 생성하기 """

        new_coupon_policy = CouponPolicy.init_entity(**request.validated_data)

        new_coupon_policy.save()

        return new_coupon_policy
