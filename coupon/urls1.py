from django.urls import path

from .views.v1.coupon_view import V1CouponIssueView

urlpatterns = [

    path("issue", view=V1CouponIssueView.as_view(), name="v1-coupon-issue"),

]
