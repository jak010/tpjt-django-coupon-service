from django.urls import path

from .views.v2.v2_coupon_policy_view import V2CouponPolicyView, V2CouponPolicyDetailView

urlpatterns = [

    path("policy", view=V2CouponPolicyView.as_view(), name="v2-coupon-policy"),

    path("policy/<int:coupon_policy_id>", view=V2CouponPolicyDetailView.as_view(), name="v2-coupon-policy-detail"),

]
