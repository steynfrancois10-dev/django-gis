from django.contrib import admin
from FarmApp.models import Farm, Crop, Farmer

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    readonly_fields = ('last_update', 'last_update_by')
    list_display = ('name', 'location', 'size_hectares')  # 3 columns
    search_fields = ('name',)  # search by farm name
    list_filter = ('size_hectares',)  # filter by size
    

    def save_model(self, request, obj, form, change):
        obj.last_update_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    readonly_fields = ('last_update', 'last_update_by')
    list_display = ('crop_type', 'farm', 'planted_area')  # 3 columns
    search_fields = ('crop_type', 'farm__name')  # search by crop type and farm
    list_filter = ('crop_type',)  # filter by crop type
    raw_id_fields = ('farm',)  # searchable dropdown for foreign key
    

    def save_model(self, request, obj, form, change):
        obj.last_update_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'experience_years')  # 3 columns
    search_fields = ('name', 'farm__name')  # search by farmer name or farm
    list_filter = ('experience_years',)  # filter by experience
    raw_id_fields = ('farm',)  # searchable dropdown for foreign key

