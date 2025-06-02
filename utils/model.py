from django.db import models

from django.forms import model_to_dict


class TimeField(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self):
        _to_dict = model_to_dict(self)
        _to_dict['created_at'] = self.created_at
        _to_dict['updated_at'] = self.updated_at

        return _to_dict
