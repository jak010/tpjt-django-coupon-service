from django.db import models


class TimeField(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        abstract = True
