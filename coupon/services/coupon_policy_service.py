from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction

from coupon.models.coupon_policy import CouponPolicy

if TYPE_CHECKING:
    from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateSchema


class CouponPolicyService:

    @transaction.atomic
    def create_coupon_policy(self,
                             coupon_policy_command: CouponPolicyCreateSchema.CouponPolicyCreateRequest
                             ):
        new_coupon_policy = CouponPolicy.with_command(
            command=coupon_policy_command
        )
        new_coupon_policy.save()

        return new_coupon_policy
