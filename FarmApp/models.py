from django.db import models

class Farm(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)  # e.g., "lat,lon"
    size_hectares = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.location})"

class Crop(models.Model):
    CROP_CHOICES = [
        ('wheat', 'Wheat'),
        ('corn', 'Corn'),
        ('rice', 'Rice'),
        ('soybean','Soybean'),
        ('sunflower','Sunflower'),
    ]
    crop_type = models.CharField(max_length=10, choices=CROP_CHOICES)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    planted_area = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.crop_type} on {self.farm.name}"

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (Farm: {self.farm.name})"



    