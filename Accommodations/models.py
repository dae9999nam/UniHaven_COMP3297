from django.db import models

# Create your models here.

class Accommodation(models.Model):
    RENTAL_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ]

    # Existing fields
    #accommodation_id = models.CharField(max_length=50, primary_key=True)
    location = models.CharField(max_length=200)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_period = models.CharField(max_length=7, choices=RENTAL_PERIOD_CHOICES, default='monthly')
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    distance_from_campus = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.location} (${self.rental_price})"