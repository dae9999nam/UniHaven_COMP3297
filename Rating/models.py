from django.db import models

# Create your models here.
class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    score = models.IntegerField(range=(0,6)) #The scale should be 0 - 5 , total 6 values
    comment = models.TextField(blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.score}"