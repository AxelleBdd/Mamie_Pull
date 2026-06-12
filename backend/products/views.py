import json

from django.http import HttpResponseNotAllowed
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


@extend_schema(responses=ProductSerializer)
@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([AllowAny])
def products_api(request, product_id=None, category_id=None):
    # Authenticate and authorize write operations with JWT
    if request.method in ["POST", "PUT", "DELETE"]:
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)
        if not request.user.is_staff:
            return Response({"error": "Admin permission required"}, status=403)

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
    return Response(serializer.data)


# GET product by id
def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# GET products by category
def get_products_by_category(category_id):
    products = Product.objects.filter(category_id=category_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# POST product
def create_product(request, body):
    if not body.get("title"):
        return Response({"error": "title is required"}, status=400)
    if not body.get("description"):
        return Response({"error": "description is required"}, status=400)
    if not body.get("category"):
        return Response({"error": "category is required"}, status=400)
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
        return Response(serializer.data, status=201)
    except ValueError:
        return Response(
            {"error": "an error occurred while creating the product"}, status=400
        )


# PUT product
def update_product(product_id, body):
    if product_id is None:
        return Response({"error": "Product ID required"}, status=400)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
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
    return Response(serializer.data)


# DELETE product
def delete_product(product_id):
    if product_id is None:
        return Response({"error": "Product ID required"}, status=400)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    product.delete()
    return Response({}, status=204)
