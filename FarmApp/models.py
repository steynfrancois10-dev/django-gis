from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Area

class BaseModel(models.Model):
    last_update = models.DateTimeField(auto_now=True)
    last_update_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_updates"
    )

    class Meta:
        abstract = True

class Farm(BaseModel):
    name = models.CharField(max_length=150)
    # Use a GIS field if you have GDAL/GeoDjango, otherwise change to JSONField/text
    boundary = gis_models.PolygonField(srid=4326, null=True, blank=True)
    size_hectares = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # calculate area in hectares if boundary exists
        if self.boundary:
            # transform to a projected CRS appropriate for area calc (example uses UTM zone 35S: EPSG 32735)
            try:
                # clone=True returns transformed geometry without changing original srid
                projected = self.boundary.transform(32735, clone=True)
                # Area(projected).ha gives hectares (requires contrib.gis.measure)
                self.size_hectares = round(Area(projected).ha, 2)
            except Exception:
                # fallback: keep size_hectares None if transform fails
                self.size_hectares = self.size_hectares or None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Crop(BaseModel):
    name = models.CharField(max_length=150)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="crops", null=True, blank=True)
    # Using PolygonField to allow small polygon or use PointField if you prefer
    boundary = gis_models.PolygonField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.name

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



    