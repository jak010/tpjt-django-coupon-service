from django.urls import path

from django.http.response import HttpResponse

from .views.coupon_policy_view import CouponPolicyView, CouponPolicyDetailView

urlpatterns = [
    path("", view=lambda x: HttpResponse(status=200)),
    path("/policy", view=CouponPolicyView.as_view(), name="coupon-policy"),
    path("/policy/<int:coupon_policy_id>", view=CouponPolicyDetailView.as_view(), name="coupon-policy-detail"),

]
