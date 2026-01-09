from django.urls import path
from .views import category_api

urlpatterns = [
    path("categories/", category_api),
    path("categories/<int:category_id>/", category_api),
]