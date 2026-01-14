from django.urls import path
from .views import products_api

urlpatterns = [
    path("", products_api),
    path("<int:products_id>/", products_api),
]
