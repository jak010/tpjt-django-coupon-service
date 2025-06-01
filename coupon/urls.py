from django.urls import path

from .views.coupon_policy_view import CouponPolicyView, CouponPolicyDetailView
from .views.coupon_view import CouponIssueView, CouponUseView, CouponCancelView, CouponDetailView

urlpatterns = [
    path("", view=CouponDetailView.as_view(), name="coupon-detail"),
    path("/issue", view=CouponIssueView.as_view(), name="coupon-issue"),
    path("/use", view=CouponUseView.as_view(), name="coupon-use"),
    path("/cancel", view=CouponCancelView.as_view(), name="coupon-cancel"),

    path("/policy", view=CouponPolicyView.as_view(), name="coupon-policy"),
    path("/policy/<int:coupon_policy_id>", view=CouponPolicyDetailView.as_view(), name="coupon-policy-detail"),

]
