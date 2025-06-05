from __future__ import annotations

import enum
from datetime import datetime, timezone
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
            discount_type=cls.of_status(value=discount_type).value,
            discount_value=discount_value,
            minimum_order_amount=minimum_order_amount,
            maximum_order_amount=maximum_order_amount,
            total_quantity=total_quantity,
            start_time=start_time,
            end_time=end_time
        )

    @classmethod
    def of_status(cls, value: str):
        if value == cls.DiscountType.FIXED_AMOUNT.value:
            return cls.DiscountType.FIXED_AMOUNT

        elif value == cls.DiscountType.PERCENT_AMOUNT.value:
            return cls.DiscountType.PERCENT_AMOUNT

        raise Exception(f"Invalid discount type: {value}")

    def get_start_time(self):
        return self.start_time.replace(tzinfo=timezone.utc)

    def get_end_time(self):
        return self.end_time.replace(tzinfo=timezone.utc)

    def is_issueable_time_coupon(self):
        """ 쿠폰이 발급 가능한 시간인지 체크하기 """

        _current = datetime.now().replace(tzinfo=timezone.utc)

        if self.start_time.replace(tzinfo=timezone.utc) < _current < self.end_time.replace(tzinfo=timezone.utc):
            return True
        return False
