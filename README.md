# Farming App — Django Lesson 4 (Function-Based Views)

This project is part of Django Lesson 4 and demonstrates how to implement **CRUD (Create, Read, Update, Delete)** functionality using Function-Based Views.
The project uses models from a simple farming system: **Farm and Crop.**
This project is part of a Django GIS learning module and demonstrates how to integrate Leaflet.js, Leaflet Draw, and GeoJSON with Django.
Users can draw farm boundaries (polygons) and crop locations (points) on an interactive map, save them to the database, and view them later.

## 🚜 Features Implemented

## 1. Interactive Mapping System

- A fully working map using Leaflet.js

- Users can draw:

    - 🟩 Farm boundaries (Polygon/Rectangle)

    - 🟡 Crop locations (Marker)

- Drawn shapes are saved in the database as GeoJSON

- Existing farms and crops load automatically when the page is opened

## 2. CRUD Functionality (Function-Based Views)

Both Farm and Crop models include full CRUD (Create, Read, Update, Delete) functionality.

### Farm Views

| Action            | View Type     | URL                   |
| ----------------- | ------------- | --------------------- |
| List all farms    | `farm_list`   | `/farms/`             |
| View farm details | `farm_detail` | `/farms/<id>/`        |
| Create a new farm | `farm_create` | `/farms/create/`      |
| Update a farm     | `farm_update` | `/farms/<id>/update/` |
| Delete a farm     | `farm_delete` | `/farms/<id>/delete/` |

### Crop Views

| Action            | View Type     | URL                   |
| ----------------- | ------------- | --------------------- |
| List all crops    | `crop_list`   | `/crops/`             |
| View crop details | `crop_detail` | `/crops/<id>/`        |
| Create a crop     | `crop_create` | `/crops/create/`      |
| Update a crop     | `crop_update` | `/crops/<id>/update/` |
| Delete a crop     | `crop_delete` | `/crops/<id>/delete/` |

## 🌾 Models Used

### Farm

- Name

- Boundary (GeoJSON Polygon)

- Automatically stored via Leaflet Draw

### Crop

- Name

- Farm (ForeignKey)

- Location (GeoJSON Point)

## 🗺️ Interactive Map Page

The **farm_map.html** page includes:

- Leaflet map centered on Potchefstroom

- Polygon + Marker drawing tools

- Auto-fill of geometry into Django forms

- Saving via the /save-geojson/ endpoint

- Display of all saved farms and crops

## 🧩 Templates

All pages extend a styled base.html containing:

- Bootstrap navigation bar

- Links to Farms, Crops, and Map

- CSRF protection + shared styles

Templates include:

- base.html

- home.html

- farm_list.html

- farm_detail.html

- farm_form.html

- farm_confirm_delete.html

- crop templates (same structure)

- farm_map.html (Leaflet map)

## ⚙️ Setup Instructions

### 1. Create virtual environment

~~~

python -m venv env

env\Scripts\activate       

~~~

### 2. Install dependencies

~~~

pip install django

~~~

### 3. Run migrations

~~~

python manage.py makemigrations
python manage.py migrate

~~~

### 4. Start the development server

~~~

python manage.py runserver

~~~

Visit: http://127.0.0.1:8000/

## 🌱 Branch Used

This work was completed on the branch:

~~~

django-lesson-4-fbv

~~~
