from typing import List, Dict

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

    @classmethod
    def failure(cls, desc):
        return cls(
            status=200,
            data={
                "message": desc
            }
        )

    @classmethod
    def page(cls, response_serializer: Serializer):
        response_serializer.is_valid(raise_exception=True)

        return cls(
            status=cls.status_code,
            data={
                "page": response_serializer.validated_data["page"],
                "per_page": response_serializer.validated_data["per_page"],
                "total_page": response_serializer.validated_data["total_page"],
                "data": response_serializer.validated_data["items"]
            }
        )


class NoContentResponse(Response):
    status_code = 201
    content_type = "application/json"

    @classmethod
    def success(cls):
        return cls(
            status=cls.status_code,
            data={
                "message": "success"
            }
        )
