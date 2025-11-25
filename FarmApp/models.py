from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Area

class Farm(models.Model):
    name = models.CharField(max_length=100)
    boundary = gis_models.PolygonField(srid=4326, null=True, blank=True)
    location = gis_models.PointField(srid=4326, null=True, blank=True)
    size_hectares = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.boundary:
            boundary_utm = self.boundary.transform(32735, clone=True)
            self.size_hectares = Area(boundary_utm).ha
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

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
    planted_area = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    boundary = gis_models.PolygonField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"{self.crop_type}"

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (Farm: {self.farm.name})"



    