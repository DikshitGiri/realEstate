from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Property(models.Model):
    property_type = models.CharField(max_length=100)  # Type of property (e.g., House, Apartment, Condo)
    location = models.CharField(max_length=255)  # Location of the property
    price_range = models.DecimalField(max_digits=10, decimal_places=2)  # Price range of the property
    image = models.ImageField(upload_to='property_images/')  # Image of the property
    details = models.TextField() 
    status=models.TextField(default='Available') # Details/description of the property
    sold_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.property_type
    
class Property_type(models.Model):
    property_type = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.property_type
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    property_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price_range = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    image = models.ImageField(upload_to='notification_images/')
    status = models.CharField(max_length=20, default='Pending')

