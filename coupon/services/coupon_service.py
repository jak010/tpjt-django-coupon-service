from __future__ import annotations

import dataclasses
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from coupon.models.coupon import Coupon, CouponPolicy

from coupon.serializer.coupon_serializer import CouponCreateSchema


class CouponService:

    def issue_coupon(self,
                     request: CouponCreateSchema.CouponCreateRequest):
        """ 쿠폰 생성하기

        Requirements
            1. 쿠폰 정책 없이 쿠폰을 생성할 수 없음
            2. 쿠폰 정책의 발급 기간이 유효하지 않을떄는 쿠폰을 생성할 수 없음
            3. 쿠폰의 발급 수량 제한이 넘어갈떄는 쿠폰을 생성할 수 없음

        """

        # HACK, 25.06.01 : Django ORM을 사용하니 Typing을 이처럼 지정해줘야함
        coupon_policy: Optional[CouponPolicy] = CouponPolicy.objects.filter(
            coupon_policy_id=request.validated_data["coupon_policy_id"]
        ).first()

        if coupon_policy is None:
            raise Exception("Coupon Policy Not Found")

        if not coupon_policy.is_issueable_time_coupon():
            raise Exception("쿠폰 발급 기간이 아닙니다.")

        if coupon_policy.total_quantity == 0:
            raise Exception("쿠폰이 모두 소진되었습니다.")

        new_coupon = Coupon.init_entity(coupon_policy=coupon_policy)
        new_coupon.save()

        return new_coupon

    def use_coupon(self):
        """ 쿠폰 사용하기 """
        raise NotImplementedError()

    def cancel_coupon(self):
        """ 쿠폰 취소하기 """
        raise NotImplementedError()

    def get_coupon(self):
        """ 쿠폰 조회 """
        raise NotImplementedError()
