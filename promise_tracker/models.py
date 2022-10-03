from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Politician(models.Model):
    pass


class Party(models.Model):
    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"


class Promise(models.Model):
    pass


class Position(models.Model):
    pass


class Evidence(models.Model):
    pass


class Source(models.Model):
    pass
