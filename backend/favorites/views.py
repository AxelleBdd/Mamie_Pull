from django.http import HttpResponseNotAllowed
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product

from .models import Favorite
from .serializers import ProductSerializer


@extend_schema(responses=ProductSerializer)
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def favorites_api(request, product_id=None):
    if request.method == "GET":
        return get_favorites(request)
    elif request.method == "POST":
        return add_favorite(request, product_id)
    elif request.method == "DELETE":
        return remove_favorite(request, product_id)

    return HttpResponseNotAllowed(["GET", "POST", "DELETE"])


# GET favorites
def get_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("product")
    serializer = ProductSerializer([f.product for f in favorites], many=True)
    return Response(serializer.data)


# POST favorite
def add_favorite(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        Favorite.objects.create(user=request.user, product=product)
        return Response(ProductSerializer(product).data, status=201)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)


# DELETE favorite
def remove_favorite(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        Favorite.objects.filter(user=request.user, product=product).delete()
        return Response({"message": "Product removed from favorites"}, status=200)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
