from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, _("English")), (LANGUAGE_KOREAN, _("Korean")))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(_("gender"), choices=GENDER_CHOICES, max_length=10, blank=True)

    bio = models.TextField(_("bio"), blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(_("language"), choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN)

    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW)

    superhost = models.BooleanField(default=False)

    def __str__(self):
        return self.username
