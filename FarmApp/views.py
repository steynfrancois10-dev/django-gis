from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Farm, Crop

from django.shortcuts import render

def home(request):
    return render(request, 'FarmApp/home.html')


class FarmListView(ListView):
    model = Farm
    template_name = "FarmApp/farm_list.html"

# Farm

class FarmDetailView(DetailView):
    model = Farm
    template_name = "FarmApp/farm_detail.html"


class FarmCreateView(CreateView):
    model = Farm
    fields = "__all__"
    template_name = "FarmApp/farm_form.html"
    success_url = reverse_lazy("farm-list")


class FarmUpdateView(UpdateView):
    model = Farm
    fields = "__all__"
    template_name = "FarmApp/farm_form.html"
    success_url = reverse_lazy("farm-list")


class FarmDeleteView(DeleteView):
    model = Farm
    template_name = "FarmApp/farm_confirm_delete.html"
    success_url = reverse_lazy("farm-list")

# Crops

class CropListView(ListView):
    model = Crop
    template_name = "FarmApp/crop_list.html"


class CropDetailView(DetailView):
    model = Crop
    template_name = "FarmApp/crop_detail.html"


class CropCreateView(CreateView):
    model = Crop
    fields = "__all__"
    template_name = "FarmApp/crop_form.html"
    success_url = reverse_lazy("crop-list")


class CropUpdateView(UpdateView):
    model = Crop
    fields = "__all__"
    template_name = "FarmApp/crop_form.html"
    success_url = reverse_lazy("crop-list")


class CropDeleteView(DeleteView):
    model = Crop
    template_name = "FarmApp/crop_confirm_delete.html"
    success_url = reverse_lazy("crop-list")

