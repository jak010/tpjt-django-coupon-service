from __future__ import annotations

import redis.exceptions
from django.db import transaction
from rest_framework.exceptions import NotFound, Throttled

from coupon.models.coupon import Coupon
from coupon.serializer.coupon_serializer import CouponCreateSchema
from coupon.services.v2.coupon_redis_service import CouponRedisService
from coupon.services.v2.coupon_state_service import CouponStateService


class CouponServiceV2:
    COUPON_QUANTITY_KEY = "coupon:quantity"
    COUPON_LOCK_KEY = "coupon:lock"
    LOCK_WAIT_TIME = 1
    LOCK_LEASE_TIME = 3

    coupon_redis_service: CouponRedisService = CouponRedisService()
    coupon_state_service: CouponStateService = CouponStateService()

    @transaction.atomic
    def issue_coupon(self,
                     request: CouponCreateSchema.CouponCreateRequest):
        """ 쿠폰 생성하기

        Requirements
            1. 쿠폰 정책 없이 쿠폰을 생성할 수 없음
            2. 쿠폰 정책의 발급 기간이 유효하지 않을떄는 쿠폰을 생성할 수 없음
            3. 쿠폰의 발급 수량 제한이 넘어갈떄는 쿠폰을 생성할 수 없음
        """
        try:
            coupon = self.coupon_redis_service.issue_coupon(request)
        except redis.exceptions.LockError:
            raise Throttled()

        self.coupon_state_service.update_coupon_state(coupon)
        return coupon

    @transaction.atomic
    def use_coupon(self, coupon_id: int, order_id: int):
        """ 쿠폰 사용하기

        1. DB에서 쿠폰을 조회 후 없으면 Exception
        2. order_id로 coupon을 사용처리
        3. CouponStateService로 쿠폰의 상태 업데이트 이후 coupon 모델 리턴

        """

        coupon = Coupon.objects.select_for_update() \
            .filter(coupon_id=coupon_id) \
            .first()
        if coupon is None:
            raise Exception("Coupon Not Found")

        coupon.use_coupon(order_id)
        self.coupon_state_service.update_coupon_state(coupon)
        return coupon

    @transaction.atomic
    def cancel_coupon(self, coupon_id: int):
        """ 쿠폰 취소하기 """
        coupon = Coupon.objects.select_for_update() \
            .filter(coupon_id=coupon_id) \
            .first()
        if coupon is None:
            raise Exception("Coupon Not Found")

        coupon.cancel_coupon()
        self.coupon_state_service.update_coupon_state(coupon)
        return coupon

    @transaction.atomic
    def get_coupon(self, coupon_id: int):
        """ 쿠폰 조회 """
        cached_coupon = self.coupon_state_service.get_coupon_state(coupon_id)
        if cached_coupon is not None:
            return cached_coupon

        coupon = Coupon.objects.filter(coupon_id=coupon_id).first()
        if coupon is None:
            raise NotFound()

        self.coupon_state_service.update_coupon_state(coupon)
        return coupon
