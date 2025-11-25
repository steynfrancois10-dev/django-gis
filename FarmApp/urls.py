from django.urls import path
from . import views
from .views import (
    home,
    farm_list, farm_detail, farm_create, farm_update, farm_delete,
    crop_list, crop_detail, crop_create, crop_update, crop_delete
)

app_name = "FarmApp"

urlpatterns = [

    # Home
    path("", home, name="home"),

    # Farm URLs
    path("farms/", farm_list, name="farm-list"),
    path("farms/create/", farm_create, name="farm-create"),
    path("farms/<int:pk>/", farm_detail, name="farm-detail"),
    path("farms/<int:pk>/update/", farm_update, name="farm-update"),
    path("farms/<int:pk>/delete/", farm_delete, name="farm-delete"),

    # Crop URLs
    path("crops/", crop_list, name="crop-list"),
    path("crops/create/", crop_create, name="crop-create"),
    path("crops/<int:pk>/", crop_detail, name="crop-detail"),
    path("crops/<int:pk>/update/", crop_update, name="crop-update"),
    path("crops/<int:pk>/delete/", crop_delete, name="crop-delete"),

    path('map/', views.farm_map, name='farm_map'),
    path('save-geojson/', views.save_geojson, name='save_geojson'), 
    path('get-geojson/', views.get_geojson, name='get_geojson'),
]
