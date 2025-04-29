from django.db import models
from rest_framework.authtoken.models import Token

class University(models.Model):
    code = models.CharField(max_length=5, unique=True)   # e.g. 'HKU'
    name = models.CharField(max_length=100)              # e.g. 'The University of Hong Kong'
    specialist_email = models.EmailField(default="") # email address for specialist to get email notification

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return f"{self.name} ({self.code})"


class ServiceAccount(models.Model):
    """
    Represents a system account (e.g., CEDARS-HKU, HKUST portal) that calls UniHaven.
    Each service account is tied to one University and has one DRF Token for authentication.
    """
    name = models.CharField(max_length=100, unique=True)
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='service_accounts'
    )
    token = models.OneToOneField(
        Token,
        on_delete=models.CASCADE,
        related_name='service_account'
    )

    class Meta:
        verbose_name = 'Service Account'
        verbose_name_plural = 'Service Accounts'

    def __str__(self):
        return f"{self.name} for {self.university.code}"
