from django.db import models

from django.forms import model_to_dict


# Info, 아래 필드 추가해줘야 model_to_dict에서 해당 속성을 읽을 수 있음
#     created_at.editable = True
#     updated_at.editable = True

class TimeField(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now=True, editable=True)

    class Meta:
        abstract = True

    def to_dict(self):
        return model_to_dict(self)
