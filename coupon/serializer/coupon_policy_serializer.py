from rest_framework import serializers

from coupon.models.coupon_policy import CouponPolicy


class CouponPolicyModel(serializers.ModelSerializer):
    class Meta:
        model = CouponPolicy
        fields = "__all__"


class CouponPolicyListSchema:
    """ 쿠폰 정책 목록(페이지네이션) 조회

    :Request
        param page <int> : 조회할 page
        param per_page <int> : page 당의 데이터 수

    : Response

    """

    class CouponPolicyListRequest(serializers.Serializer):
        page = serializers.IntegerField(default=1)
        per_page = serializers.IntegerField(
            min_value=1,
            max_value=10,
            default=10,
            required=False
        )

    class CouponPolicyListResponse(serializers.Serializer):
        items = CouponPolicyModel(many=True)

    class CouponPolicyPaginateListReponse(serializers.Serializer):
        page = serializers.IntegerField()
        per_page = serializers.IntegerField()
        total_page = serializers.IntegerField()
        items = CouponPolicyModel(many=True)


class CouponPolicyCreateSchema:
    class CouponPolicyCreateRequest(serializers.Serializer):
        name = serializers.CharField(
            help_text="쿠폰 정책명은 필수 입니다."
        )
        discount_type = serializers.ChoiceField(
            choices=[(key.name, key.value) for key in CouponPolicy.DiscountType],
            help_text="할인 타입은 필수 입니다."
        )

        discount_value = serializers.IntegerField(
            help_text="할인량은 필수 입니다."
        )
        minimum_order_amount = serializers.IntegerField(
            help_text="쿠폰 정책의 최소주문금액은 필수 입니다."
        )
        maximum_order_amount = serializers.IntegerField(
            help_text="쿠폰 정책의 최대주문금액은 필수 입니다.",
            min_value=1
        )
        total_quantity = serializers.IntegerField(
            help_text="쿠폰 정책의 전체 수량은 필수 입니다."
        )
        start_time = serializers.DateTimeField(
            help_text="쿠폰 정책의 시작날짜은 필수 입니다."
        )
        end_time = serializers.DateTimeField(
            help_text="쿠폰 정책의 종료날짜은 필수 입니다."
        )

    # HACK, 25.06.01 : 응답 데이터의 구조가 바뀌는 경우 필드를 변경해야하기 때문에 유연하지 못한 방식이다.
    class CouponPolicyCreateResponse(serializers.Serializer):
        """ 쿠폰 정책 생성 """

        class _CreteResponseData(serializers.Serializer):
            coupon_policy_id = serializers.IntegerField()
            created_at = serializers.DateTimeField()
            updated_at = serializers.DateTimeField()

        data = _CreteResponseData()
