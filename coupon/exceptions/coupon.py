from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class InvalidIssuedTimesCoupon(APIException):
    status_code = 400
    default_detail = _('쿠폰 발급시간이 유효하지 않음')

class NotEnoughCoupon(APIException):
    status_code = 400
    default_detail = _('쿠폰 수량을 확인해주세요')