from __future__ import annotations

import datetime
import enum
import uuid

from django.db import models

from utils.model import TimeField
from .coupon_policy import CouponPolicy


def generate_random_order_id():
    return uuid.uuid4().hex


class Coupon(TimeField):
    class Meta:
        db_table = "coupon"
        ordering = ['-coupon_id']

    class Status(enum.Enum):
        AVAILABLE = "AVAILABLE"
        USED = "USED"
        EXPIRED = "EXPIRED"
        CANCELLED = "CANCELLED"

    coupon_id = models.AutoField(primary_key=True)

    coupon_code = models.CharField(max_length=6)

    coupon_policy = models.ForeignKey(CouponPolicy, on_delete=models.SET_NULL, null=True, default=None)
    status = models.CharField(choices=[(k.name, k.value) for k in Status], max_length=10)

    order_id = models.CharField(max_length=36)

    used_at = models.DateTimeField(null=True)

    @classmethod
    def init_entity(cls, coupon_policy: CouponPolicy):
        return cls(
            coupon_code=cls.generate_coupon_code(),
            coupon_policy=coupon_policy,
            status=cls.Status.AVAILABLE.value,
            order_id=generate_random_order_id(),
            used_at=None,
        )

    @classmethod
    def of_status(cls, value):
        if value is not None:
            return [k for k in cls.Status if k.value == value][0]
        raise Exception(f"Invalid status: {value}")

    @classmethod
    def generate_coupon_code(cls):
        return str(uuid.uuid4().hex)[0:6]

    def use_coupon(self, order_id: str = None):
        """ 쿠폰 사용처리하기 """
        self.status = self.Status.USED.value
        self.order_id = order_id if order_id is not None else self.order_id
        self.used_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.save()
        return self

    def cancel_coupon(self):
        """ 쿠폰 취소처리하기 """
        self.status = self.Status.CANCELLED.value
        self.updated_at = datetime.datetime.now()
        self.save()
        return self
