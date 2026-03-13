from django.urls import path

from .views import products_api

urlpatterns = [
    path("", products_api),
    path("<int:product_id>/", products_api),
    path("category/<int:category_id>/", products_api),
]
