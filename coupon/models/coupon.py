from __future__ import annotations

import enum

from django.db import models

from utils.model import TimeField
from .coupon_policy import CouponPolicy


# Create your models here.

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

    coupon_code = models.CharField(
        max_length=6
    )

    coupon_policy = models.ForeignKey(CouponPolicy, on_delete=models.SET_NULL, null=True, default=None)
    status = models.CharField(choices=[(k.name, k.value) for k in Status], max_length=10)

    order_id = models.CharField(max_length=36)

    used_at = models.DateTimeField()
