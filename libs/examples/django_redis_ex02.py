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

import datetime
import json
import os
import threading
from dataclasses import dataclass, asdict

from django.core.serializers.json import DjangoJSONEncoder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

from django.core.cache import cache


@dataclass
class Member:
    member_id: int
    name: str
    created_at: datetime.datetime

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), cls=DjangoJSONEncoder)


class AcquiredLockFailed(Exception):
    """ Lock 획득 실패 예외 """


class MemberRedisService:

    def __init__(self):
        self.temp_disk = {}

    def execute(self, member: Member):
        member_cache_key = f"member:{member.member_id}:{member.name}"
        lock_key = f"lock:{member_cache_key}"

        lock = cache.lock(lock_key, timeout=3, blocking_timeout=1)

        try:
            acquired_lock = lock.acquire(blocking=True)
            if acquired_lock:
                print(f"Lock 획득 성공: {acquired_lock}, {threading.get_ident()}")
                self.temp_disk[member_cache_key] = member.to_json()
                cache.set(member_cache_key, member.to_dict())
            else:
                print(f"Lock 획득 실패 : {acquired_lock}, {threading.get_ident()}")
        except Exception as e:
            print(e)

    def setup(self, member: Member):
        member_cache_key = f"member:{member.member_id}:{member.name}"

        # cache.get(member_cache_key)

        cache.set(member_cache_key, 0)

    def distribute_execute(self, member: Member):
        import time
        time.sleep(1)
        member_cache_key = f"member:{member.member_id}:{member.name}"
        lock_key = f"lock:{member_cache_key}"

        with cache.lock(lock_key, timeout=2, blocking_timeout=2) as lock:
            print(f"Lock 획득 성공: {lock}, {threading.get_ident()}")
            self.temp_disk[member_cache_key] = member.to_json()
            cache.incr(member_cache_key)

        # lock = cache.lock(lock_key, timeout=2, blocking_timeout=2)
        # acquired_lock = lock.acquire(blocking=True)

        # if acquired_lock:
        #     print(f"Lock 획득 성공: {acquired_lock}, {threading.get_ident()}")
        #     r = cache.set(member_cache_key, member.to_dict())
        #     lock.release()
        # else:
        #     raise AcquiredLockFailed(f"Lock 획득 실패 : {acquired_lock}, {threading.get_ident()}")


if __name__ == '__main__':
    cached_member = Member(
        member_id=1,
        name="test",
        created_at=datetime.datetime.now())

    service = MemberRedisService()
    service.setup(cached_member)

    ths = []
    for _ in range(10):
        new_member = Member(
            member_id=1,
            name="test",
            created_at=datetime.datetime.now()
        )

        th = threading.Thread(target=service.distribute_execute, args=(new_member,))
        ths.append(th)

    for th in ths:
        th.start()
    for th in ths:
        th.join()
