from django.urls import path

from .views.coupon_policy_view import CouponPolicyView, CouponPolicyDetailView
from .views.coupon_view import CouponView

urlpatterns = [
    path("", view=CouponView.as_view(), name="coupon"),

    path("/policy", view=CouponPolicyView.as_view(), name="coupon-policy"),
    path("/policy/<int:coupon_policy_id>", view=CouponPolicyDetailView.as_view(), name="coupon-policy-detail"),

]
