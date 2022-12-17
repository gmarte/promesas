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

class BaseModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
 
    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    is_anonymous = models.BooleanField(default=True)
    def __str__(self):
        return self.username
    @property
    def get_user(self):
        if self.is_anonymous:
            return "anonymous"
        else:
            return self.username


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
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='parties', null=True)
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
    @property
    def promise_count(self):
        return self.politician_promises.all().count()


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
        return f"{self.title}"
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
    url = models.CharField(max_length=200)
    type = models.CharField(max_length=2,
                            choices=TYPES_CHOICES,
                            default=PHOTO)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{ self.TYPES_CHOICES[0][int(self.type)] }:: {self.url}"


class Promise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_kpi = models.FloatField()
    rating = models.ForeignKey(
        Rating, related_name="ratings", on_delete=models.CASCADE)
    fuentes = models.ManyToManyField(Source, related_name="promise_sources")
    politician = models.ForeignKey(Politician, related_name="politician_promises", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} :: {self.rating.title}" 


class Evidence(models.Model):
    title = models.CharField(max_length=200)
    fuentes = models.ManyToManyField(Source, related_name="evidense_sources")
    promise = models.ForeignKey(
        Promise, on_delete=models.CASCADE, related_name="evidences")
    kpi = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
