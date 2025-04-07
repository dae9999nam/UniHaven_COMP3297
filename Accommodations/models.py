from django.db import models

# Create your models here.

class Accommodation(models.Model):
    RENTAL_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ]

    # Existing fields
    accommodation_id = models.IntegerField(primary_key=True,default=0) #Need this part to be automatically done by django
    name = models.CharField(max_length=200, default="empty")
    address = models.CharField(max_length=200)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_period = models.CharField(max_length=7, choices=RENTAL_PERIOD_CHOICES, default='monthly')
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    distance_from_campus = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.uploaded_date