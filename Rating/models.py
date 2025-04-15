from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Accommodations.models import Accommodation

# Create your models here.
class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    # Set accommodation as Foreignkey
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    score = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)]) #The scale should be 0 - 5 , total 6 values
    comment = models.TextField(blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.score}"