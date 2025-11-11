from django.urls import path
from . import views

urlpatterns = [
    path('farms/', views.farm_list, name='farm_list'),
]
