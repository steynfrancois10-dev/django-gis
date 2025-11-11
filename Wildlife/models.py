from django.contrib.auth.models import User
from django.db import models  # ✅ use standard Django models (no GIS)

# Create your models here.
class PropertyType(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'
        db_table = 'property_type'


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        db_table = 'province'


class Organisation(models.Model):
    """Organisation model."""
    name = models.CharField(unique=True, max_length=250)
    short_code = models.CharField(max_length=50, null=False, blank=True)
    national = models.BooleanField(null=True, blank=True)
    province = models.ForeignKey(
        Province,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Property(models.Model):
    """Property model."""
    name = models.CharField(max_length=300, unique=True)
    short_code = models.CharField(max_length=50, null=False, blank=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    property_type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING)
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)
    
    # ✅ Replace PointField with simple coordinate fields
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class TaxonRank(models.Model):
    """Taxon rank model."""
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taxon Rank"
        verbose_name_plural = "Taxon Ranks"


class Taxon(models.Model):
    """Taxon model."""
    scientific_name = models.CharField(max_length=250, unique=True)
    common_name_varbatim = models.CharField(max_length=250, null=True, blank=True)
    taxon_rank = models.ForeignKey(TaxonRank, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.scientific_name


class AnnualPopulation(models.Model):
    """Annual Population model."""
    year = models.PositiveIntegerField()
    total = models.IntegerField()
    adult_male = models.IntegerField(null=True, blank=True)
    adult_female = models.IntegerField(null=True, blank=True)
    juvenile_male = models.IntegerField(null=True, blank=True)
    juvenile_female = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    area_available_to_species = models.FloatField(default=0.0)
    sub_adult_total = models.IntegerField(null=True, blank=True)
    sub_adult_male = models.IntegerField(null=True, blank=True)
    sub_adult_female = models.IntegerField(null=True, blank=True)
    juvenile_total = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.property.name} {self.year}"

    class Meta:
        verbose_name = "Annual Population"
        verbose_name_plural = "Annual Populations"
        ordering = ["-year"]
