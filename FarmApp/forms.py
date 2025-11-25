from django import forms
from leaflet.forms.widgets import LeafletWidget
from .models import Farm, Crop
from django.contrib.gis.forms import OSMWidget

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = "__all__"
        widgets = {
            "location": LeafletWidget(),  # POINT
            'boundary': forms.HiddenInput(),  # POLYGON
        }


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = "__all__"
        widgets = {
            'location': forms.HiddenInput(),
            "boundary": LeafletWidget(),
        }
