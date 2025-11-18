# Farming App — Django Lesson 3 (Class-Based Views & CRUD)

This project is part of Django Lesson 3 and demonstrates how to implement **CRUD (Create, Read, Update, Delete)** functionality using Class-Based Views.
The project uses models from a simple farming system: **Farm, Crop, and Farmer.**

## 🚜 Features Implemented

## 1. Homepage

- A styled landing page with a navigation bar.

- Provides links to all Farm and Crop views.

## 2. Class-Based Views (CBVs) Added

For each of the two selected models (Farm and Crop), the full set of CRUD views was implemented:

### Farm Views

| Action               | View Type        | URL                   |
| -------------------- | ---------------- | --------------------- |
| List all farms       | `FarmListView`   | `/farms/`             |
| View farm details    | `FarmDetailView` | `/farms/<id>/`        |
| Create new farm      | `FarmCreateView` | `/farms/create/`      |
| Update existing farm | `FarmUpdateView` | `/farms/<id>/update/` |
| Delete farm          | `FarmDeleteView` | `/farms/<id>/delete/` |

### Crop Views

| Action            | View Type             | URL                   |
| ----------------- | --------------------- | --------------------- |
| List all crops    | `CropListView`        | `/crops/`             |
| View crop details | `CropDetailView`      | `/crops/<id>/`        |
| Create new crop   | `CropCreateView`      | `/crops/create/`      |
| Update crop       | `CropUpdateView`      | `/crops/<id>/update/` |
| Delete crop       | `/crops/<id>/delete/` |                       |

## 🌾 Models Used

The farming application includes the following models:

### Farm

- Name

- Location

- Size (hectares)

### Crop

- Crop type

- Farm (ForeignKey)

- Planted area

### *Farmer (not used in CBV task but part of dataset)*

- Name

- Farm

- Years of experience

## 🧩 Templates

All pages extend a custom base.html that includes:

- A dark Bootstrap navigation bar

- Links to Farms and Crops sections

- Bootstrap styling

Templates included:

- home.html

- farm_list.html

- farm_detail.html

- farm_form.html

- farm_confirm_delete.html

- Same structure for Crop templates

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

django-lesson-3-cbv

~~~
