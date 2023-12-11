from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    # null = True allows database entries to have null values.
    # blank = True allows forms to be submitted with this value as empty.
    age = models.PositiveIntegerField(null=True, blank=True)