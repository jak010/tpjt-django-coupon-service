import pytest

from coupon.models.coupon_policy import CouponPolicy

import datetime


@pytest.mark.django_db
def test_coupon_policy_model():
    """ 쿠폰 정책 생성 테스트 """

    coupon_policy = CouponPolicy.init_entity(
        name="[테스트]쿠폰 정책 생성",
        description="[테스트]쿠폰 정책 생성",
        discount_type=CouponPolicy.DiscountType.FIXED_AMOUNT,
        discount_value=1000,
        minimum_order_amount=10000,
        maximum_order_amount=100000,
        total_quantity=10,
        start_time=datetime.datetime.now(),
        end_time=datetime.datetime.now()
    )
    coupon_policy.save()

    assert coupon_policy.name == "[테스트]쿠폰 정책 생성"
    assert coupon_policy.discount_value == 1000
    assert coupon_policy.minimum_order_amount == 10000
