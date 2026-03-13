from django.urls import path

from .views import category_api

urlpatterns = [
    path("", category_api),
    path("<int:category_id>/", category_api),
]
