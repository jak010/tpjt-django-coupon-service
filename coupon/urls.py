from django.urls import path

from django.http.response import HttpResponse

from .views.coupon_policy_view import CouponPolicyView

urlpatterns = [
    path("", view=lambda x: HttpResponse(status=200)),
    path("/policy", view=CouponPolicyView.as_view(), name="coupon-policy"),

]
