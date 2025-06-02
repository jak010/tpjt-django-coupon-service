import json

from django.db import transaction

from django_redis import get_redis_connection
from redis.client import Redis

from django.core.serializers.json import DjangoJSONEncoder


from coupon.models import CouponPolicy
from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateSchema


class CouponPolicyServiceV2:
    COUPON_QUANTITY_KEY = "coupon:quantity"
    COUPON_POLICY_KEY = "coupon:policy"

    redis_connection: Redis = get_redis_connection()

    @transaction.atomic
    def create_coupon_policy(self,
                             request: CouponPolicyCreateSchema.CouponPolicyCreateRequest
                             ):
        """ 쿠폰 정책 생성하기 """

        new_coupon_policy = CouponPolicy.init_entity(**request.validated_data)
        new_coupon_policy.save()

        # Redis에 초기 수량 설정하기
        quantity_key = f"{self.COUPON_QUANTITY_KEY}:{new_coupon_policy.coupon_policy_id}"
        atomic_quantity = self.redis_connection.get(quantity_key)
        if atomic_quantity is None:
            self.redis_connection.set(quantity_key, new_coupon_policy.total_quantity)


        # Redis에 정책 정보 저장하기
        policy_json = json.dumps(new_coupon_policy.to_dict(), cls=DjangoJSONEncoder)
        policy_key = f"{self.COUPON_POLICY_KEY}:{new_coupon_policy.coupon_policy_id}"
        self.redis_connection.set(policy_key, policy_json)

        return new_coupon_policy
