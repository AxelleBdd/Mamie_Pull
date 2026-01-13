import json

from .models import Product
from django.http import HttpResponseNotAllowed, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

def product_api(request, product_id=None):
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
    data = [
        {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "category": product.category,
            "image": product.image
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)

#GET product by id
def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    
    return JsonResponse({
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "category": product.category,
        "image": product.image
    })

# POST product
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(body):
    product = Product.objects.create(
        name=body.get("name")
    )
    return JsonResponse({
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "category": product.category,
        "image": product.image
    }, status=201)

#PUT product
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
    
    return JsonResponse({
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "category": product.category,
        "image": product.image
    })

#DELETE product
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