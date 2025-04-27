from django.db import models
import requests
import xml.etree.ElementTree as ET
import math
from enum import Enum

# Coordiates Extraction
def get_coordinates(address):
    """
    Calls the AddressLookUp API using a free-text address query and returns:
      - Longitude (float)
      - Latitude (float)
      - GeoAddress (string)
    If the API call fails or the data can’t be parsed, returns (None, None, None).
    """
    # For a free-text GET request, set the parameter 'q' to the address.
    # Only take address to improve accuracy, no building nanme included
    params = {"q": address, "n":1}
    #url params
    """ "q": "KING'S COLLEGE OLD BOYS' ASSOCIATION PRIMARY SCHOOL", # input address element information (mandatory; URL-encoded(percent-encoded)); 
        "n": 1, #range in 1-200, default=200, based on the assumption thaat the first result provided by API will be for the correct location
        "t" - # tolerance on returned record scores (optional; range: 0-80; default: 35);
        "b" - # enable/disable basic searching mode, default disabled (optional; range: 0 or 1; default: 0). 
    """    
    url = "https://www.als.gov.hk/lookup"
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException:
        return None, None, None

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            # Based on your schema, these elements reside in <GeospatialInformation>
            latitude_el = root.find(".//GeospatialInformation/Latitude")
            longitude_el = root.find(".//GeospatialInformation/Longitude")
            # Get the GeoAddress from its XML element. According to the schema, it is located
            # within a Feature's properties, so we use the path ".//GeoAddress".
            GeoAddress_el = root.find(".//GeoAddress")
            if latitude_el is not None and longitude_el is not None and GeoAddress_el is not None:
                # Return the coordinate values as floats and GeoAddress.
                return float(longitude_el.text), float(latitude_el.text), GeoAddress_el.text
        except ET.ParseError:
            return None, None, None
    return None, None, None

# Distance Calculation
def equirectangular_distance(lat1, long1, lat2, long2):
    """
    Calculates the distance between two points (in decimal degrees)
    using the equirectangular approximation.
    Returns the distance in meters.
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(long1)
    lon2_rad = math.radians(long2)
    
    # Compute differences in radians
    delta_lon = lon2_rad - lon1_rad
    delta_lat = lat2_rad - lat1_rad

    # Adjust the longitude difference by the cosine of the average latitude
    x = delta_lon * math.cos((lat1_rad + lat2_rad) / 2)
    y = delta_lat
    
    R = 6371000
    distance = math.sqrt(x * x + y * y) * R
    return distance

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
    type = models.CharField(max_length=100, default="") #accommodation type added
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_period = models.CharField(max_length=7, choices=RENTAL_PERIOD_CHOICES, default="monthly")
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()

    # logitude and latitude are obtained by Address Lookup Service API
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    # GeoAddress added
    GeoAddress = models.CharField(max_length=200, default="")

    availability_status = models.BooleanField(default=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.accommodation_id} {self.name}"
    
    def save(self, *args, **kwargs):
        # When the address is provided and coordinates are not set (or are set to the default 0.0),
        # fetch the coordinates using the AddressLookUp API.
        if self.address and (self.longitude == 0.0 and self.latitude == 0.0 and self.GeoAddress == ""):
            lon, lat, geo = get_coordinates(self.address)
            if lon is not None and lat is not None and geo is not None:
                self.longitude = lon
                self.latitude = lat
                self.GeoAddress = geo
        # Call the original save() method to save the instance.
        super().save(*args, **kwargs)


class Campus_Premises(Enum):
     # The enum value tuple is (Display Name, latitude, longitude)
    HKU_MAIN_CAMPUS = ("Main Campus", 22.28405, 114.13784)
    SASSON = ("Sasson Road Campus", 22.2675, 114.12881)
    SWIRE = ("Swire Institute of Marine Science", 22.20805, 114.26021)
    KADOORIE = ("Kadoorie Centre", 22.43022, 114.11429)
    DENTISTRY = ("Faculty of Dentistry", 22.28649, 114.14426)
    HKUST_CAMPUS = ("HKUST Main Campus", 22.33584, 114.26355)
    CUHK_CAMPUS = ("CUHK Main Campus", 22.41907, 114.20693)