from __future__ import annotations

import enum
from datetime import datetime

from django.db import models

from utils.model import TimeField


class CouponPolicy(TimeField):
    class Meta:
        db_table = "coupon_policy"
        ordering = ['-coupon_policy_id']

    class DiscountType(enum.Enum):
        """ 쿠폰 할인정책 필드 """
        FIXED_AMOUNT = "FIXED_AMOUNT"  # 정액 할인
        PERCENTAGE = "PERCENT_AMOUNT"  # 정률 할인

    coupon_policy_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=36)
    description = models.CharField(max_length=72)

    discount_type = models.CharField(choices=[(key.name, key.value) for key in DiscountType], null=False, max_length=24)
    discount_value = models.PositiveIntegerField(choices=[(key.name, key.value) for key in DiscountType], null=False)

    minimum_order_amount = models.PositiveIntegerField(null=False)
    maximum_order_amount = models.PositiveIntegerField(null=False)
    total_quantity = models.PositiveIntegerField(null=False)

    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    @classmethod
    def init_entity(cls,
                    name: str,
                    description: str,
                    discount_type: DiscountType,
                    discount_value: int,
                    minimum_order_amount: int,
                    maximum_order_amount: int,
                    total_quantity: int,
                    start_time: datetime,
                    end_time: datetime
                    ):
        return cls(
            name=name,
            description=description,
            discount_type=discount_type.value,
            discount_value=discount_value,
            minimum_order_amount=minimum_order_amount,
            maximum_order_amount=maximum_order_amount,
            total_quantity=total_quantity,
            start_time=start_time,
            end_time=end_time
        )
