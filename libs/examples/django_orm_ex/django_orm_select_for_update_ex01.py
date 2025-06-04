"""
Django ORM의 select_for_update를 사용하여 동시성 및 데드락 상황을 테스트하는 스크립트.

이 스크립트는 두 개의 독립된 프로세스(worker1, worker2)를 통해 동일한 데이터베이스 레코드에 대해
서로 다른 순서로 select_for_update를 사용하여 잠금을 시도함으로써 데드락이 발생할 수 있는
조건을 재현하고 실험하는 목적으로 사용된다.

구성:
- Django 설정을 초기화하여 외부 스크립트에서도 ORM 사용 가능하도록 설정
- CouponPolicy 모델을 select_for_update로 잠금
- 두 개의 프로세스를 병렬 실행하여 잠금 충돌 또는 데드락 발생 여부 관찰

주의:
- 실제 운영 환경이 아닌 테스트/개발 환경에서만 실행할 것
- 데드락이 발생할 경우 무한 대기 상태가 될 수 있음
- DB 엔진(InnoDB 등)에 따라 데드락이 감지되면 트랜잭션이 강제 롤백되고 예외가 발생할 수 있음

사용 예시:
    python this_script.py
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()  # 반드시 setup 호출

from coupon.models.coupon import CouponPolicy
from django.db import transaction
from multiprocessing import Process


def worker1():
    with transaction.atomic():
        c = CouponPolicy.objects.select_for_update().filter(coupon_policy_id=14).first()
        c = CouponPolicy.objects.select_for_update().filter(coupon_policy_id=15).first()
        print(f" worker1:{c.coupon_policy_id}")


def worker2():
    with transaction.atomic():
        c = CouponPolicy.objects.select_for_update().filter(coupon_policy_id=15).first()
        c = CouponPolicy.objects.select_for_update().filter(coupon_policy_id=14).first()
        print(f" worker2:{c.coupon_policy_id}")


if __name__ == '__main__':
    t1 = Process(target=worker1)
    t2 = Process(target=worker2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
