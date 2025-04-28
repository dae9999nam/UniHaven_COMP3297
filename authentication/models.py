from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token

class University(models.TextChoices):
    HKU   = 'HKU',  'The University of Hong Kong - HKU'
    HKUST = 'HKUST','Hong Kong University of Science and Technology - HKUST'
    CUHK  = 'CUHK', 'The Chinese University of Hong Kong - CUHK'


class ServiceAccount(models.Model):
    name       = models.CharField(max_length=100, unique=True)
    university = models.CharField(max_length=5, choices=settings.UNIVERSITY_CHOICES)
    token      = models.OneToOneField(Token, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.university})"
