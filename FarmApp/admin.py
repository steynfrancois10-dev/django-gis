from django.contrib import admin
from .models import Farm, Crop, Farmer

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location',)  
    search_fields = ('name',)
    list_filter = ('name',)  
    raw_id_fields = ()  

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_type', 'farm',)  
    search_fields = ('crop_type',)
    list_filter = ('crop_type',)
    raw_id_fields = ('farm',)

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm',)
    search_fields = ('name',)
    list_filter = ('farm',)
    raw_id_fields = ('farm',)


