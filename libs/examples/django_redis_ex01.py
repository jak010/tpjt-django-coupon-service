import datetime
import json
import os
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


class MemberRedisService:

    def __init__(self):
        self.temp_disk = {}

    def write_back(self, member: Member):
        member_cache_key = f"member:{member.member_id}:{member.name}"

        is_cached = cache.get(member_cache_key)

        if is_cached is None:
            self.temp_disk[member_cache_key] = member.to_json()
            cache.set(member_cache_key, member.to_dict())

    def read_from_redis(self, member: Member):
        """ Example, django_redis

        Redis로 부터 데이터 읽기
         - 기본적으로 byte 로 읽어들인다. (b'{"member_id": 1, "name": "test"}')
         -

        """
        member_cache_key = f"member:{member.member_id}:{member.name}"

        is_cached = cache.get(member_cache_key)

        print(is_cached)


if __name__ == '__main__':
    new_member = Member(
        member_id=1,
        name="test",
        created_at=datetime.datetime.now()
    )

    service = MemberRedisService()
    # service.write_back(new_member)

    service.read_from_redis(new_member)
