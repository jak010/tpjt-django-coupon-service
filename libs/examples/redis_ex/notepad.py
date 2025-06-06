""" django_redis lock 예제

이 스크립트는 Django 캐시 시스템을 활용한 Redis 기반 분산 락 동작을 검증하기 위한 테스트 코드입니다.

주요 목적:
- `MemberRedisService.execute()` 메서드 내에서 Redis 락(`cache.lock`)을 이용하여 다중 스레드 환경에서 동일한 키에 대해 경쟁 조건(race condition)이 발생하지 않도록 제어할 수 있는지를 검증합니다.
- 동일한 `member_id`와 `name`을 가진 `Member` 객체를 여러 스레드에서 동시에 처리할 때,
  - 락을 획득한 스레드만 캐시에 데이터를 쓰도록 되어 있는지
  - 락 획득 성공 및 실패 여부가 올바르게 출력되는지
  - 메모리 임시 저장소(`self.temp_disk`)에도 락 획득 성공 시에만 저장이 되는지를 테스트합니다.

기타 사항:
- Django의 `DjangoJSONEncoder`를 사용하여 datetime 객체를 포함한 `Member` 인스턴스를 JSON으로 직렬화합니다.
- 테스트 실행 시, 10개의 스레드가 동시에 같은 `Member` 데이터를 처리하게 하여 락 동작을 시뮬레이션합니다.
- Django 설정 모듈은 로컬 개발 환경용(`config.settings.local`)으로 가정합니다.

"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

from django.core.cache import cache

coupon_policy_id = 162

cache_key = f"coupon:quantity:{coupon_policy_id}"

cached = cache.get(cache_key)
