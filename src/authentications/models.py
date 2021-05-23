from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import MaxValueValidator


class User(AbstractUser):
    name = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(upload_to="profile_images", blank=True)
    mobile = models.PositiveIntegerField(blank=True, null=True,
                                         validators=[MaxValueValidator(9999999999)])
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.CharField(blank=True, null=True, max_length=60)
