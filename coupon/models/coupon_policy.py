from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models

from utils.model import TimeField

if TYPE_CHECKING:
    from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateRequest


class CouponPolicy(TimeField):
    class Meta:
        db_table = "coupon_policy"
        ordering = ['-coupon_policy_id']

    class DiscountType(enum.Enum):
        """ 쿠폰 할인정책 필드 """
        FIXED_AMOUNT = "FIXED_AMOUNT"  # 정액 할인
        PERCENT_AMOUNT = "PERCENT_AMOUNT"  # 정률 할인

        @classmethod
        def of(cls, value):
            if value == cls.FIXED_AMOUNT.value:
                return cls.FIXED_AMOUNT.value
            elif value == cls.PERCENT_AMOUNT.value:
                return cls.PERCENT_AMOUNT.value

            raise Exception(f"Invalid discount type: {value}")

    coupon_policy_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=36)
    description = models.CharField(max_length=72, null=True)

    discount_type = models.CharField(choices=[(key.name, key.value) for key in DiscountType], null=False, max_length=24)
    discount_value = models.PositiveIntegerField(null=False)

    minimum_order_amount = models.PositiveIntegerField(null=False)
    maximum_order_amount = models.PositiveIntegerField(null=False)
    total_quantity = models.PositiveIntegerField(null=False)

    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    @classmethod
    def init_entity(cls,
                    name: str,
                    discount_type: str,
                    discount_value: int,
                    maximum_order_amount: int,
                    minimum_order_amount: int,
                    total_quantity: int,
                    start_time: datetime,
                    end_time: datetime
                    ):
        return cls(
            name=name,
            discount_type=cls.DiscountType.of(discount_type),
            discount_value=discount_value,
            minimum_order_amount=minimum_order_amount,
            maximum_order_amount=maximum_order_amount,
            total_quantity=total_quantity,
            start_time=start_time,
            end_time=end_time
        )
