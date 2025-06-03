from __future__ import annotations

from typing import Optional

from django.core.cache import cache
from django.db import transaction
from django_redis import get_redis_connection
from redis import Redis

from coupon.exceptions.coupon import InvalidIssuedTimesCoupon
from coupon.models.coupon import Coupon, CouponPolicy
from coupon.serializer.coupon_serializer import CouponCreateSchema


class CouponRedisService:
    COUPON_QUANTITY_KEY = "coupon:quantity"
    COUPON_LOCK_KEY = "coupon:lock"
    LOCK_WAIT_TIME = 1
    LOCK_LEASE_TIME = 3

    @transaction.atomic
    def issue_coupon(self,
                     request: CouponCreateSchema.CouponCreateRequest) -> Coupon:
        """ 쿠폰 생성하기

        Requirements
            1. 쿠폰 정책 없이 쿠폰을 생성할 수 없음
            2. 쿠폰 정책의 발급 기간이 유효하지 않을떄는 쿠폰을 생성할 수 없음
            3. 쿠폰의 발급 수량 제한이 넘어갈떄는 쿠폰을 생성할 수 없음
        """

        quantity_key = f"{self.COUPON_QUANTITY_KEY}:{request.validated_data['coupon_policy_id']}"
        lock_key = f"{self.COUPON_LOCK_KEY}:{request.validated_data['coupon_policy_id']}"
        redis_connection: Redis = get_redis_connection()

        redis_lock = cache.lock(lock_key, timeout=self.LOCK_WAIT_TIME, blocking_timeout=self.LOCK_LEASE_TIME)

        try:
            acquierd_lock = redis_lock.acquire(blocking=True)
            if acquierd_lock:

                # HACK, 25.06.01 : Django ORM을 사용하니 Typing을 이처럼 지정해줘야함
                coupon_policy: Optional[CouponPolicy] = CouponPolicy.objects.select_for_update().filter(
                    coupon_policy_id=request.validated_data["coupon_policy_id"]
                ).first()

                if coupon_policy is None:
                    raise Exception("Coupon Policy Not Found")

                if not coupon_policy.is_issueable_time_coupon():
                    raise InvalidIssuedTimesCoupon()

                remain_quantity = redis_connection.decr(quantity_key)
                if remain_quantity < 0:
                    raise Exception("쿠폰이 모두 소진되었습니다.")

                # 쿠폰 정책에 설정된 수량보다 많은 쿠폰을 생성할 수 없음
                new_coupon = Coupon.init_entity(coupon_policy=coupon_policy)
                new_coupon.save()

                return new_coupon

        except Exception as e:
            raise Exception("쿠폰 발급 도중 오류가 발생했습니다.")
        finally:
            redis_lock.release()
