from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse 
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry

from .models import Farm, Crop
from .forms import FarmForm, CropForm 


def home(request):
    return render(request, 'FarmApp/home.html')

# -----------------------------
# FARM FBV
# -----------------------------

def farm_list(request):
    qs = Farm.objects.all().order_by('-last_update')
    paginator = Paginator(qs, 10)  # 10 per page
    page = request.GET.get('page')
    farms = paginator.get_page(page)
    return render(request, "FarmApp/farm_list.html", {"farms": farms})


def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    return render(request, "FarmApp/farm_detail.html", {"farm": farm})


def farm_create(request):
    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            # last_update_by = current user
            farm.last_update_by = request.user if request.user.is_authenticated else None
            farm.save()
            messages.success(request, "Farm created successfully.")
            return redirect(reverse("FarmApp:farm-list"))
    else:
        form = FarmForm()
    return render(request, "FarmApp/farm_form.html", {"form": form, "action": "Create"})


def farm_update(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == "POST":
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.last_update_by = request.user if request.user.is_authenticated else farm.last_update_by
            farm.save()
            messages.success(request, "Farm updated successfully.")
            return redirect(reverse("FarmApp:farm-detail", kwargs={"pk": farm.pk}))
    else:
        form = FarmForm(instance=farm)
    return render(request, "FarmApp/farm_form.html", {"form": form, "action": "Update"})


def farm_delete(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == "POST":
        farm.delete()
        messages.success(request, "Farm deleted.")
        return redirect(reverse("FarmApp:farm-list"))
    return render(request, "FarmApp/farm_confirm_delete.html", {"farm": farm})


# -----------------------------
# CROP FBV
# -----------------------------

def crop_list(request):
    qs = Crop.objects.select_related('farm').all().order_by('-last_update')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    crops = paginator.get_page(page)
    return render(request, "FarmApp/crop_list.html", {"crops": crops})


def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    return render(request, "FarmApp/crop_detail.html", {"crop": crop})


def crop_create(request):
    if request.method == "POST":
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.last_update_by = request.user if request.user.is_authenticated else None
            crop.save()
            messages.success(request, "Crop created successfully.")
            return redirect(reverse("FarmApp:crop-list"))
    else:
        form = CropForm()
    return render(request, "FarmApp/crop_form.html", {"form": form, "action": "Create"})


def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == "POST":
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.last_update_by = request.user if request.user.is_authenticated else crop.last_update_by
            crop.save()
            messages.success(request, "Crop updated successfully.")
            return redirect(reverse("FarmApp:crop-detail", kwargs={"pk": crop.pk}))
    else:
        form = CropForm(instance=crop)
    return render(request, "FarmApp/crop_form.html", {"form": form, "action": "Update"})


def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == "POST":
        crop.delete()
        messages.success(request, "Crop deleted.")
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

@require_POST
def save_geojson(request):
    """
    Expects JSON body:
    {
      "geojson": { ... geometry ... },
      "type": "farm" or "crop",
      "name": "Optional name"
    }
    Uses CSRF token header; request.user used to set last_update_by.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    geojson = data.get('geojson')
    item_type = data.get('type')
    name = data.get('name', 'Unnamed')

    if not geojson or not item_type:
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        # Build GEOS geometry (expects geometry object)
        geom = GEOSGeometry(json.dumps(geojson), srid=4326)
    except Exception as e:
        return JsonResponse({"error": f"Invalid geometry: {str(e)}"}, status=400)

    if item_type == 'farm':
        farm = Farm.objects.create(name=name, boundary=geom, last_update_by=request.user if request.user.is_authenticated else None)
        return JsonResponse({"status": "success", "id": farm.id})
    elif item_type == 'crop':
        crop = Crop.objects.create(name=name, boundary=geom, last_update_by=request.user if request.user.is_authenticated else None)
        return JsonResponse({"status": "success", "id": crop.id})
    else:
        return JsonResponse({"error": "Invalid type"}, status=400)
    
def get_geojson(request):
    farms = []
    crops = []
    for f in Farm.objects.all():
        if f.boundary:
            farms.append({
                "id": f.id,
                "name": f.name,
                "geojson": json.loads(f.boundary.geojson)
            })
    for c in Crop.objects.all():
        if c.boundary:
            crops.append({
                "id": c.id,
                "name": c.name,
                "geojson": json.loads(c.boundary.geojson)
            })
    return JsonResponse({"farms": farms, "crops": crops})
