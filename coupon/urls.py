from django.urls import path

from django.http.response import HttpResponse

urlpatterns = [
    path("", view=lambda x: HttpResponse(status=200))
]
