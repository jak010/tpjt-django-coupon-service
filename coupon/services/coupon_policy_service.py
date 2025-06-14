from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.paginator import Paginator, EmptyPage
from django.db import transaction

from coupon.models.coupon_policy import CouponPolicy
from contrib.result import PaginateResult

if TYPE_CHECKING:
    from coupon.serializer.coupon_policy_serializer import CouponPolicyCreateSchema, CouponPolicyListSchema


class CouponPolicyService:

    @transaction.atomic
    def create_coupon_policy(self,
                             request: CouponPolicyCreateSchema.CouponPolicyCreateRequest
                             ):
        """ 쿠폰 정책 생성하기 """

        new_coupon_policy = CouponPolicy.init_entity(**request.validated_data)
        new_coupon_policy.save()

        return new_coupon_policy

    @transaction.atomic
    def get_all_coupon_policy(self,
                              request: CouponPolicyListSchema.CouponPolicyListRequest
                              ) -> PaginateResult:
        """ 쿠폰 정책 목록조회 """

        paginator = Paginator(CouponPolicy.objects.all(), request.validated_data["per_page"])

        try:
            coupon_policies = paginator.page(request.validated_data["page"])
        except EmptyPage as e:
            print(e)

            coupon_policies = paginator.page(paginator.num_pages)

        return PaginateResult(
            page=request.validated_data["page"],
            per_page=request.validated_data["per_page"],
            total_page=paginator.num_pages,
            items=[
                coupon_policy.to_dict() for coupon_policy in coupon_policies.object_list
            ]  # HACK, 25-06-01 : Lazy Load 때문에 List 안 걸어주면 View 레벨에서 Transaction이 한번 더 걸림
        )

    @transaction.atomic()
    def get_coupon_policy(self, coupon_policy_id: int):
        coupon_policy = CouponPolicy.objects.filter(coupon_policy_id=coupon_policy_id)

        if coupon_policy is None:
            raise Exception("Coupon Policy Not Found")

        return coupon_policy.first()
