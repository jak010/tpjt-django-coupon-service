from __future__ import annotations

from typing import Optional

from django.db import transaction
from rest_framework.exceptions import NotFound

from coupon.exceptions.coupon import InvalidIssuedTimesCoupon, NotEnoughCoupon
from coupon.models.coupon import Coupon, CouponPolicy
from coupon.serializer.coupon_serializer import CouponCreateSchema


class CouponRDBService:

    @transaction.atomic
    def issue_coupon(self,
                     request: CouponCreateSchema.CouponCreateRequest):
        """ 쿠폰 생성하기

        Requirements
            1. 쿠폰 정책 없이 쿠폰을 생성할 수 없음
            2. 쿠폰 정책의 발급 기간이 유효하지 않을떄는 쿠폰을 생성할 수 없음
            3. 쿠폰의 발급 수량 제한이 넘어갈떄는 쿠폰을 생성할 수 없음

        Note:
            쿠폰 발급 로직의 문제
                1. lock이 잡혀있지 않기 떄문에 설정된 쿠폰 발급 수량보다 더 많은 쿠폰이 생성될 있음
                2. 성능이슈, 매 요청마다 쿠폰 수를 카운트 하는 쿼리 실행
                  - 쿠폰 수가 많아질 수록 카운트 쿼리의 성능이 저하될 수 있음

        """
        # HACK, 25.06.01 : Django ORM을 사용하니 Typing을 이처럼 지정해줘야함
        coupon_policy: Optional[CouponPolicy] = CouponPolicy.objects \
            .select_for_update() \
            .filter(coupon_policy_id=request.validated_data["coupon_policy_id"]) \
            .first()

        if coupon_policy is None:
            raise Exception("Coupon Policy Not Found")

        if not coupon_policy.is_issueable_time_coupon():
            raise InvalidIssuedTimesCoupon()

        # 쿠폰 정책에 설정된 수량보다 많은 쿠폰을 생성할 수 없음
        issued_coupon_count = Coupon.objects.filter(coupon_policy=coupon_policy).count()
        if coupon_policy.total_quantity <= issued_coupon_count:
            raise NotEnoughCoupon()

        new_coupon = Coupon.init_entity(coupon_policy=coupon_policy)
        new_coupon.save()

        return new_coupon

    @transaction.atomic
    def use_coupon(self, coupon_id: int):
        """ 쿠폰 사용하기 """
        coupon: Optional[Coupon] = Coupon.objects.filter(
            coupon_id=coupon_id
        ).first()

        if coupon is None:
            raise Exception("Coupon Not Found")

        coupon.use_coupon()

        return coupon

    @transaction.atomic
    def cancel_coupon(self, coupon_id: int):
        """ 쿠폰 취소하기 """
        coupon: Optional[Coupon] = Coupon.objects.filter(
            coupon_id=coupon_id
        ).first()

        if coupon is None:
            raise Exception("Coupon Not Found")

        coupon.cancel_coupon()

        return coupon

    @transaction.atomic
    def get_coupon(self, coupon_id: int):
        """ 쿠폰 조회 """
        coupon: Optional[Coupon] = Coupon.objects.filter(
            coupon_id=coupon_id
        ).first()

        if coupon is None:
            raise NotFound()

        return coupon
