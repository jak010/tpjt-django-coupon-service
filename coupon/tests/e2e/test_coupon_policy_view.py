import json

import pytest
from rest_framework.test import APIRequestFactory, APIClient


@pytest.mark.django_db
class TestCreateCouponPolicyView:

    def setup_class(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.request_url = '/api/v1/coupon/policy'

    def test_create_fixed_amount_coupon_policy_view(self):
        """ 쿠폰 정책, 정액 할인 생성 테스트 """

        # Arrange
        request_data = {
            "name": "여름 프로모션 10% 할인",
            "discount_type": "FIXED_AMOUNT",
            "discount_value": 10,
            "minimum_order_amount": 30000,
            "maximum_order_amount": 150000,
            "total_quantity": 1000,
            "start_time": "2025-07-01",
            "end_time": "2025-07-31"
        }

        # Act
        response = self.client.post(
            self.request_url,
            content_type="application/json",
            data=json.dumps(request_data)
        )
        # Arrange

        # Assert
        assert response.status_code == 200

    def test_create_percent_amount_coupon_policy_view(self):
        """ 쿠폰 정책, 정률 할인 생성 테스트 """
        # Arrange
        request_data = {
            "name": "여름 프로모션 10% 할인",
            "discount_type": "PERCENTAGE",
            "discount_value": 10,
            "minimum_order_amount": 30000,
            "maximum_order_amount": 150000,
            "total_quantity": 1000,
            "start_time": "2025-07-01T00:00:00Z",
            "end_time": "2025-07-31T23:59:59Z"
        }

        # Act
        request = self.client.post(
            self.request_url,
            content_type="application/json",
            data=json.dumps(request_data)
        )

        # Assert
        assert request.status_code == 200
