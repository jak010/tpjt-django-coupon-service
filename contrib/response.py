from rest_framework.response import Response

from rest_framework.serializers import Serializer


class NormalResponse(Response):
    status_code = 200
    content_type = "application/json"

    @classmethod
    def success(cls, response_serializer: Serializer):
        return cls(
            status=cls.status_code,
            data=response_serializer.data
        )
