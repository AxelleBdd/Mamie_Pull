import json

from .models import Product
from django.http import HttpResponseNotAllowed, JsonResponse
from .serializers import ProductSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

def products_api(request, product_id=None):
    if request.method == "GET":
        if product_id is None:
            return get_products()
        else:
            return get_product(product_id)
    
    elif request.method == "POST":
        body = json.loads(request.body)
        return create_product(body)
    
    elif request.method == "PUT":
        body = json.loads(request.body)
        return update_product(product_id, body)
    
    elif request.method == "DELETE":
        return delete_product(product_id)
    
    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])

#GET all products
def get_products():
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)

#GET product by id
def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

# POST product
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(body):
    product = Product.objects.create(
        title=body.get("title"),
        description=body.get("description"),
        category_id=body.get("category"),
        image=body.get("image")
    )
    serializer = ProductSerializer(product)
    return JsonResponse(serializer.data, status=201)

#PUT product
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(product_id, body):
    if product_id is None:
        return JsonResponse(
            {"error": "Product ID required"},
            status=400
        )
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    
    product.title = body.get("title", product.title)
    product.description = body.get("description", product.description)
    product.category = body.get("category", product.category)
    product.image = body.get("image", product.image)
    product.save()
    
    serializer = ProductSerializer(product)
    return JsonResponse(serializer.data)

#DELETE product
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(product_id):
    if product_id is None:
        return JsonResponse(
            {"error": "Product ID required"},
            status=400
        )
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    
    product.delete()
    return JsonResponse({}, status=204)