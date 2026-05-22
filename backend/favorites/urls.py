from django.urls import path

from .views import favorites_api

urlpatterns = [
    path("", favorites_api, name="favorites"),
    path("<int:product_id>/", favorites_api, name="favorites-detail"),
]
