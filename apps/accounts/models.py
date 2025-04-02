from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.helper import keys,choices
from apps.helper.models import TimeStampedUUIDModel

User = get_user_model()

######### Profile model ########
class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=choices.Gender.choices,
        default=choices.Gender.OTHER,
        max_length=20,
    )
    country = models.CharField( max_length=50,verbose_name=_("Country"), default="India", blank=True, null=True
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.email}'s profile"
