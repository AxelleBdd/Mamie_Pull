import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product
from .serializers import ProductSerializer


@csrf_exempt
def products_api(request, product_id=None, category_id=None):
    # Authenticate and authorize write operations with JWT
    if request.method in ["POST", "PUT", "DELETE"]:
        auth = JWTAuthentication()
        try:
            auth_result = auth.authenticate(request)
        except AuthenticationFailed:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if auth_result is None:
            return JsonResponse({"error": "Authentication required"}, status=401)
        request.user, request.auth = auth_result
        if not request.user.is_staff:
            return JsonResponse({"error": "Admin permission required"}, status=403)

    if request.method == "GET":
        if product_id is not None:
            return get_product(product_id)
        if category_id is not None:
            return get_products_by_category(category_id)
        else:
            return get_products()

    elif request.method == "POST":
        body = json.loads(request.body)
        return create_product(request, body)

    elif request.method == "PUT":
        body = json.loads(request.body)
        return update_product(product_id, body)

    elif request.method == "DELETE":
        return delete_product(product_id)

    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])


# GET all products
def get_products():
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)


# GET product by id
def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)


# GET products by category
def get_products_by_category(category_id):
    products = Product.objects.filter(category_id=category_id)
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)


# POST product
def create_product(request, body):
    # Validate required fields
    if not body.get("title"):
        return JsonResponse({"error": "title is required"}, status=400)
    if not body.get("description"):
        return JsonResponse({"error": "description is required"}, status=400)
    if not body.get("category"):
        return JsonResponse({"error": "category is required"}, status=400)

    try:
        product = Product.objects.create(
            title=body.get("title"),
            description=body.get("description"),
            category_id=body.get("category"),
            image=body.get("image"),
            sizes=body.get("sizes", []),
            created_by=request.user,
        )
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, status=201)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)


# PUT product
def update_product(product_id, body):
    if product_id is None:
        return JsonResponse({"error": "Product ID required"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    # Only update fields that are provided
    if "title" in body:
        product.title = body.get("title")
    if "description" in body:
        product.description = body.get("description")
    if "category" in body:
        product.category_id = body.get("category")
    if "image" in body:
        product.image = body.get("image")
    if "sizes" in body:
        product.sizes = body.get("sizes")

    product.save()

    serializer = ProductSerializer(product)
    return JsonResponse(serializer.data)


# DELETE product
def delete_product(product_id):
    if product_id is None:
        return JsonResponse({"error": "Product ID required"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    product.delete()
    return JsonResponse({}, status=204)
