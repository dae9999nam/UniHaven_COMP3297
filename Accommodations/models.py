from django.db import models
import requests
import xml.etree.ElementTree as ET

def get_coordinates(address):
    """
    Calls the AddressLookUp API and returns (longitude, latitude) as floats.
    If the API call fails or the data can’t be parsed, returns (None, None).
    """
    # For a free-text GET request, set the parameter 'q' to the address.
    # Only take address to improve accuracy, no building nanme included
    params = {"q": address}
    url = "https://www.als.gov.hk/lookup"
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException:
        return None, None

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            # Based on your schema, these elements reside in <GeospatialInformation>
            latitude_el = root.find(".//GeospatialInformation/Latitude")
            longitude_el = root.find(".//GeospatialInformation/Longitude")
            if latitude_el is not None and longitude_el is not None:
                # Return the coordinate values as floats.
                return float(longitude_el.text), float(latitude_el.text)
        except ET.ParseError:
            return None, None
    return None, None

class Accommodation(models.Model):
    RENTAL_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ]
    
    # Existing fields
    accommodation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default="empty")
    address = models.CharField(max_length=200)
    type = models.CharField(max_length=100, default="") #accommodation type
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    #rental period - available start date?
    rental_period = models.CharField(max_length=7, choices=RENTAL_PERIOD_CHOICES, default="monthly")
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    availability_status = models.BooleanField(default=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.uploaded_date
    
    def save(self, *args, **kwargs):
        # When the address is provided and coordinates are not set (or are set to the default 0.0),
        # fetch the coordinates using the AddressLookUp API.
        if self.address and (self.longitude == 0.0 and self.latitude == 0.0):
            lon, lat = get_coordinates(self.address)
            if lon is not None and lat is not None:
                self.longitude = lon
                self.latitude = lat
        # Call the original save() method to save the instance.
        super().save(*args, **kwargs)