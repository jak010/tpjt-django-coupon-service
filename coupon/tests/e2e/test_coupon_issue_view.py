import json

import pytest
from rest_framework.test import APIRequestFactory, APIClient

from datetime import datetime, timedelta

from coupon.models.coupon_policy import CouponPolicy


@pytest.mark.django_db
class TestCreateCouponView:
    """ TC

    성공 케이스
        - 유효한 coupon_policy_id를 사용하고, 발급 가능 시간 내에 있으며, 쿠폰 수량이 남아 있는 경우 쿠폰이 정상적으로 발급된다.

    실패 케이스
        - 존재하지 않는 coupon_policy_id를 사용할 경우 Exception("Coupon Policy Not Found")가 발생한다.
        - 쿠폰 정책이 존재하지만 발급 기간이 아닌 경우 Exception("쿠폰 발급 기간이 아닙니다.")가 발생한다.
        - 쿠폰 수량이 모두 소진된 경우 Exception("쿠폰이 모두 소진되었습니다.")가 발생한다.

    엣지 / 추가 케이스
        - 쿠폰 수량이 1개일 때는 발급이 가능하지만, 그 이후에는 수량이 0이 되어 발급이 실패해야 한다.
        - request.validated_data에 coupon_policy_id가 없는 경우 KeyError 또는 별도의 유효성 검사가 필요하다.
        - Coupon.save() 호출 시 DB 예외가 발생하는 경우를 고려해 예외 처리 여부를 테스트할 수 있다.

    """

    def setup_class(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.request_url = '/api/v1/coupon/issue'

    @pytest.mark.parametrize("discount_type", ["FIXED_AMOUNT", "PERCENT_AMOUNT"])
    def test_create_coupon_issue(self, discount_type):
        """ 쿠폰 생성 API 테스트.

        이 테스트는 다음을 검증합니다:
          주어진 조건의 정액 할인 쿠폰 정책을 생성한 뒤, 해당 쿠폰 정책 ID를 포함한 POST 요청을 보냈을 때,
           API가 정상적으로 200 OK 응답을 반환하는지 확인합니다.
        """

        # Arrange
        new_coupon_policy = CouponPolicy.init_entity(
            start_time=datetime.now() - timedelta(days=1),
            end_time=datetime.now() + timedelta(days=1),
            discount_type=discount_type,
            discount_value=10,
            minimum_order_amount=30000,
            maximum_order_amount=150000,
            total_quantity=1,
            name="여름 프로모션 10% 할인"
        )
        new_coupon_policy.save()

        # Act
        response = self.client.post(
            self.request_url,
            content_type="application/json",
            data=json.dumps({
                "coupon_policy_id": new_coupon_policy.pk
            })
        )

        # Assert
        assert response.status_code == 200

    def test_create_failure_when_coupon_policy_not_found(self):
        """ 쿠폰 생성 API 테스트."""
        # Arrange

        # 존재하지 않는 coupon_policy_id를 사용
        request_data = json.dumps({
            "coupon_policy_id": 1231231231
        })

        # Act
        response = self.client.post(
            self.request_url,
            data=request_data
        )

        # Assert
        assert response.status_code == 200
