import json

from django_redis import get_redis_connection
from coupon.models.coupon import Coupon

from redis import Redis


class CouponStateService:
    redis_client: Redis = get_redis_connection()

    COUPON_STATE_KEY = "coupon:state"

    def update_coupon_state(self, coupon: Coupon):
        """ 쿠폰 상태를 Redis에 저장 """

        state_key = f"{self.COUPON_STATE_KEY}:{coupon.coupon_id}"

        try:
            bucket = self.redis_client.get(state_key)
            bucket.set(json.dumps(coupon.to_dict()))
        except Exception as e:
            raise Exception("쿠폰 상태 업데이트 중 에러가 발생했습니다.")

    def get_coupon_state(self, coupon_id: int):
        state_key = f"{self.COUPON_STATE_KEY}:{coupon_id}"

        try:
            bucket = self.redis_client.get(state_key)
            return json.loads(bucket.decode())
        except Exception as e:
            raise Exception("쿠폰 상태 조회 중 에러가 발생했습니다.")
