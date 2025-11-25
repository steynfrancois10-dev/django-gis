from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Farm, Crop
from .forms import FarmForm, CropForm  
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry

def home(request):
    return render(request, 'FarmApp/home.html')

# -----------------------------
# FARM FBV
# -----------------------------

def farm_list(request):
    farms = Farm.objects.all()
    return render(request, "FarmApp/farm_list.html", {"farms": farms})


def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    return render(request, "FarmApp/farm_detail.html", {"farm": farm})


def farm_create(request):
    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("FarmApp:farm-list"))
    else:
        form = FarmForm()
    return render(request, "FarmApp/farm_form.html", {"form": form})


def farm_update(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == "POST":
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            return redirect(reverse("FarmApp:farm-detail", pk=farm.pk))
    else:
        form = FarmForm(instance=farm)
    return render(request, "FarmApp/farm_form.html", {"form": form})


def farm_delete(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == "POST":
        farm.delete()
        return redirect(reverse("FarmApp:farm-list"))
    return render(request, "FarmApp/farm_confirm_delete.html", {"farm": farm})


# -----------------------------
# CROP FBV
# -----------------------------

def crop_list(request):
    crops = Crop.objects.all()
    return render(request, "FarmApp/crop_list.html", {"crops": crops})


def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    return render(request, "FarmApp/crop_detail.html", {"crop": crop})


def crop_create(request):
    if request.method == "POST":
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("FarmApp:crop-list"))
    else:
        form = CropForm()
    return render(request, "FarmApp/crop_form.html", {"form": form})


def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == "POST":
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect(reverse("FarmApp:crop-detail", pk=crop.pk))
    else:
        form = CropForm(instance=crop)
    return render(request, "FarmApp/crop_form.html", {"form": form})


def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == "POST":
        crop.delete()
        return redirect(reverse("FarmApp:crop-list"))
    return render(request, "FarmApp/crop_confirm_delete.html", {"crop": crop})

# -----------------------------
# MAP FBV
# -----------------------------

def farm_map(request):
    if request.method == 'POST':
        if 'boundary' in request.POST:
            form = FarmForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'location' in request.POST:
            form = CropForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect(reverse('FarmApp:farm_map'))

    farms = Farm.objects.all()
    crops = Crop.objects.all()
    farms_geojson = serialize('geojson', farms, geometry_field='boundary')
    crops_geojson = serialize('geojson', crops, geometry_field='location')

    context = {
        'farms_geojson': farms_geojson,
        'crops_geojson': crops_geojson,
        'farm_form': FarmForm(),
        'crop_form': CropForm(),
    }
    return render(request, 'FarmApp/farm_map.html', context)

    from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .forms import FarmForm, CropForm

@csrf_exempt
def save_geojson(request):
    """
    Receives GeoJSON from Leaflet Draw and saves it as a Farm or Crop.
    """

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
        geojson = data.get("geojson")
        item_type = data.get("type")      # "farm" or "crop"
        name = data.get("name", "Unnamed")

        if not geojson:
            return JsonResponse({"error": "Missing GeoJSON"}, status=400)

        geom = GEOSGeometry(json.dumps(geojson))

        # ---------------------------------------------
        # SAVE FARM
        # ---------------------------------------------
        if item_type == "farm":
            farm = Farm.objects.create(
                name=name,
                boundary=geom,
                size_hectares=0  # TEMP, will update later
            )
            return JsonResponse({"success": True, "id": farm.id})

        # ---------------------------------------------
        # SAVE CROP
        # ---------------------------------------------
        elif item_type == "crop":
            crop = Crop.objects.create(
                name=name,
                boundary=geom
            )
            return JsonResponse({"success": True, "id": crop.id})

        else:
            return JsonResponse({"error": "Invalid type"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_geojson(request):
    farms = [{
        "id": f.id,
        "name": f.name,
        "type": "farm",
        "geojson": json.loads(f.boundary.geojson) if f.boundary else None
    } for f in Farm.objects.all()]

    crops = [{
        "id": c.id,
        "name": c.name,
        "type": "crop",
        "geojson": json.loads(c.boundary.geojson) if c.boundary else None
    } for c in Crop.objects.all()]

    return JsonResponse({"farms": farms, "crops": crops})
