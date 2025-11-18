from .views import home
from django.urls import path
from .views import (
    FarmListView, FarmDetailView, FarmCreateView, FarmUpdateView, FarmDeleteView,
    CropListView, CropDetailView, CropCreateView, CropUpdateView, CropDeleteView
)

urlpatterns = [

    # Farm URLS
    path("farms/", FarmListView.as_view(), name="farm-list"),
    path("farms/create/", FarmCreateView.as_view(), name="farm-create"),
    path("farms/<int:pk>/", FarmDetailView.as_view(), name="farm-detail"),
    path("farms/<int:pk>/update/", FarmUpdateView.as_view(), name="farm-update"),
    path("farms/<int:pk>/delete/", FarmDeleteView.as_view(), name="farm-delete"),

    # Crops URLS
    path("crops/", CropListView.as_view(), name="crop-list"),
    path("crops/create/", CropCreateView.as_view(), name="crop-create"),
    path("crops/<int:pk>/", CropDetailView.as_view(), name="crop-detail"),
    path("crops/<int:pk>/update/", CropUpdateView.as_view(), name="crop-update"),
    path("crops/<int:pk>/delete/", CropDeleteView.as_view(), name="crop-delete"),

    path('', home, name='home'),

]
