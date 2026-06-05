from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.models import Product

from .models import Favorite
from .serializers import ProductSerializer


@csrf_exempt
def favorites_api(request, product_id=None):
    # Authenticate with JWT for all requests
    auth = JWTAuthentication()
    try:
        auth_result = auth.authenticate(request)
    except AuthenticationFailed:
        return JsonResponse({"error": "Authentication required"}, status=401)
    if auth_result is None:
        return JsonResponse({"error": "Authentication required"}, status=401)
    request.user, request.auth = auth_result

    if request.method == "GET":
        return get_favorites(request)
    elif request.method == "POST":
        return add_favorite(request, product_id)
    elif request.method == "DELETE":
        return remove_favorite(request, product_id)

    return HttpResponseNotAllowed(["GET", "POST", "DELETE"])


# GET all favorite products for the authenticated user
def get_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user).select_related("product")
    serializer = ProductSerializer(
        [favorite.product for favorite in favorites], many=True
    )
    return JsonResponse(serializer.data, safe=False)


# POST add a product to favorites
def add_favorite(request, product_id):
    user = request.user
    try:
        product = Product.objects.get(id=product_id)
        Favorite.objects.create(user=user, product=product)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, status=201)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)


# DELETE remove a product from favorites
def remove_favorite(request, product_id):
    user = request.user
    try:
        product = Product.objects.get(id=product_id)
        Favorite.objects.filter(user=user, product=product).delete()
        return JsonResponse({"message": "Product removed from favorites"}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
