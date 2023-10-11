from django.db import models

# Create your models here.


class Property(models.Model):
    property_type = models.CharField(max_length=100)  # Type of property (e.g., House, Apartment, Condo)
    location = models.CharField(max_length=255)  # Location of the property
    price_range = models.DecimalField(max_digits=10, decimal_places=2)  # Price range of the property
    image = models.ImageField(upload_to='property_images/')  # Image of the property
    details = models.TextField()  # Details/description of the property

    def __str__(self):
        return self.property_type
    
class Property_type(models.Model):
    property_type = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.property_type

