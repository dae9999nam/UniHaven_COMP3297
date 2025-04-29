from django.db import models
from Accommodations.models import Accommodation

# Create your models here.
class Reservation(models.Model):

    Reservation_status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    # Existing fields
    #Primary key
    reservation_id = models.AutoField(primary_key=True)
    #Link to the accommodation being booked
    accommodation = models.ForeignKey(Accommodation , on_delete=models.CASCADE) 
    #Whos making the reservation
    contact = models.CharField(max_length=50, default="empty")
    start_date = models.DateField()
    end_date = models.DateField()
    updated_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Reservation_status_choices, default='pending')

    # def __str__(self):
    #     return self.created_time