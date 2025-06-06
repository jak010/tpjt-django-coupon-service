import json

from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction

from coupon.models import CouponPolicy
from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateSchema


class CouponPolicyServiceV2:
    COUPON_QUANTITY_KEY = "coupon:quantity"
    COUPON_POLICY_KEY = "coupon:policy"

    @transaction.atomic
    def create_coupon_policy(self,
                             request: CouponPolicyCreateSchema.CouponPolicyCreateRequest
                             ):
        """ 쿠폰 정책 생성하기

        Note:
            쿠폰 정책 생성 시, Redis에 초기수량과 정책 정보를 저장한다.

        """

        new_coupon_policy = CouponPolicy.init_entity(**request.validated_data)
        new_coupon_policy.save()

        # Redis에 초기 수량 설정하기
        quantity_key = f"{self.COUPON_QUANTITY_KEY}:{new_coupon_policy.coupon_policy_id}"
        atomic_quantity = cache.get(quantity_key)
        if atomic_quantity is None:
            cache.set(quantity_key, new_coupon_policy.total_quantity)

        # Redis에 정책 정보 저장하기
        policy_json = json.dumps(new_coupon_policy.to_dict(), cls=DjangoJSONEncoder)
        policy_key = f"{self.COUPON_POLICY_KEY}:{new_coupon_policy.coupon_policy_id}"
        cache.set(policy_key, policy_json)

        return new_coupon_policy

    @transaction.atomic
    def get_coupon_policy(self, coupon_policy_id: int):
        """ 쿠폰 정책 조회 - coupon_policy_id로 Redis에 쿠폰 정책 찾기

        1. Redis에 쿠폰 정책이 없다면 DB에 접근해서 Return (DB에 없다면 NotFound )
        2. Redis에 쿠폰 정책이 있다면 Return 하기

        """

        _policy_key = f"{self.COUPON_POLICY_KEY}:{coupon_policy_id}"

        bucket = self.redis_connection.get(_policy_key)
        if bucket:
            try:
                return json.loads(bucket.decode())
            except json.JSONDecodeError as e:
                raise Exception("Json Parsing Error")

        coupon_policy = CouponPolicy.objects.filter(coupon_policy_id=coupon_policy_id).first()
        if coupon_policy is None:
            raise Exception("CouponPolicy를 찾을 수 없음")
        return coupon_policy.to_dict()

    @transaction.atomic
    def get_all_coupon_policy(self):
        """ 쿠폰 정책 목록 조회 - Redis에서는 조회하지는 않는 듯 ? """
        return [item.to_dict() for item in CouponPolicy.objects.all()]
