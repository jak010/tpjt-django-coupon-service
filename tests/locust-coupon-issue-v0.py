from locust import HttpUser, task, between


class CouponIssueUser(HttpUser):
    wait_time = between(0.1, 0.5)  # 사용자 요청 간 간격 (초)

    @task
    def issue_coupon(self):
        """ Lock 이 적용되지 않는 코드에 대한 테스트  스크립트

        Note:
            이 스크립트가 테스트 대상으로 하는 Service 로직은 select .. for update를 사용하지 않았음을 가정한다.

        Goal :
            - Exception 이 발생한 직후 쿠폰이 얼마나 생성되었는가를 관찰한다.

        """
        payload = {
            "coupon_policy_id": 14
        }

        self.client.post(
            "/api/v1/coupon/issue",
            json=payload,
            headers={
                "Content-Type": "application/json"
            }
        )
