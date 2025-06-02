from django.urls import path

from .views.v2.v2_coupon_policy_view import V2CouponPolicyView

urlpatterns = [

    path("/policy", view=V2CouponPolicyView.as_view(), name="v2-coupon-policy"),

]
