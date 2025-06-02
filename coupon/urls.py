from django.urls import path

from .views.coupon_policy_view import CouponPolicyView, CouponPolicyDetailView
from .views.coupon_view import CouponIssueView, CouponUseView, CouponCancelView, CouponDetailView

urlpatterns = [
    path("/issue", view=CouponIssueView.as_view(), name="coupon-issue"),
    path("/<int:coupon_id>", view=CouponDetailView.as_view(), name="coupon-detail"),
    path("/<int:coupon_id>/use", view=CouponUseView.as_view(), name="coupon-use"),
    path("/<int:coupon_id>/cancel", view=CouponCancelView.as_view(), name="coupon-cancel"),

    path("/policy", view=CouponPolicyView.as_view(), name="coupon-policy"),
    path("/policy/<int:coupon_policy_id>", view=CouponPolicyDetailView.as_view(), name="coupon-policy-detail"),

]
