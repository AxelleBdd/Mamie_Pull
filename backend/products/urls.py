from django.urls import path

from .views import products_api

urlpatterns = [
    path("", products_api, name="product-list"),
    path("<int:product_id>/", products_api, name="product-detail"),
    path("category/<int:category_id>/", products_api, name="product-category"),
]
