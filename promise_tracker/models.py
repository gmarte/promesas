# from statistics import mode
from email.policy import default
from random import choices
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from numpy import blackman
from django_countries.fields import CountryField


class User(AbstractUser):
    pass


class Position(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Party(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    logo = models.ImageField(null=True, blank=True, upload_to='parties/')
    acronym = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.acronym + " - " + self.name

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"


class Politician(models.Model):
    PRIMARIA = '01'
    SECUNDARIA = '02'
    UNIVERSITARIO = '03'
    MAESTRIA = '04'
    DOCTORADO = '05'
    EDUCATION_CHOICES = [
        (PRIMARIA, 'Primaria'),
        (SECUNDARIA, 'Secundaria'),
        (UNIVERSITARIO, 'Universitario'),
        (MAESTRIA, 'Maestria'),
        (DOCTORADO, 'Doctorado'),
    ]
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    party = models.ManyToManyField(
        Party, through='PartyValidity', related_name='parties')
    country = CountryField()
    religion = models.CharField(max_length=64, blank=True)
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="positions")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    education = models.CharField(
        max_length=2,
        choices=EDUCATION_CHOICES,
        default=PRIMARIA,
    )
    photo = models.ImageField(null=True, blank=True, upload_to='politician/')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fname} {self.lname}"


class PartyValidity(models.Model):
    politician = models.ForeignKey(
        Politician, on_delete=models.CASCADE, null=True)
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE, null=True, blank=True)
    ini = models.DateField()
    end = models.DateField()

class Rating(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    color = models.CharField(max_length=6)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title}: {self.description}"
    class Meta:
        ordering = ['order']

class Source(models.Model):
    NEWS = '01'
    VIDEO = '02'
    PHOTO = '03'
    TYPES_CHOICES = [
        (NEWS, 'Prensa'),
        (VIDEO, 'Video'),
        (PHOTO, 'Foto'),
    ]
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=2,
                            choices=TYPES_CHOICES,
                            default=PHOTO)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Promise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_kpi = models.FloatField()
    rating = models.ForeignKey(
        Rating, related_name="ratings", on_delete=models.CASCADE)
    fuentes = models.ManyToManyField(Source, related_name="promise_sources")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)


class Evidence(models.Model):
    title = models.CharField(max_length=200)
    fuentes = models.ManyToManyField(Source, related_name="evidense_sources")
    promise = models.ForeignKey(
        Promise, on_delete=models.CASCADE, related_name="evidences")
    kpi = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
