from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):

    """Room Model Definition"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 추상모델 = 상속으로 사용하고 데이터베이스 저장용으로 사용하지 않는다.
    class Meta:
        abstract = True
