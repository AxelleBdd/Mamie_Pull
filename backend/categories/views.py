import json

from .models import Category
from django.http import HttpResponseNotAllowed, JsonResponse
from .serializers import CategorySerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

def category_api(request, category_id=None):
    if request.method == "GET":
        if category_id is None:
            return get_categories()
        else:
            return get_category(category_id)
    
    elif request.method == "POST":
        return create_category(request)
    
    elif request.method == "PUT":
        return update_category(request, category_id)
    
    elif request.method == "DELETE":
        return delete_category(category_id)
    
    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])

#GET all categories
def get_categories():
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False)

#GET category by id
def get_category(category_id):
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

# POST category
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    body = json.loads(request.body)
    category = Category.objects.create(
        name=body.get("name")
    )
    serializer = CategorySerializer(category)
    return JsonResponse(serializer.data, status=201)

#PUT category
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, category_id):
    if category_id is None:
        return JsonResponse(
            {"error": "Category ID required"},
            status=400
        )
    
    body = json.loads(request.body)
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    
    category.name = body.get("name", category.name)
    category.save()
    
    serializer = CategorySerializer(category)
    return JsonResponse(serializer.data, status=201)

#DELETE category
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(category_id):
    if category_id is None:
        return JsonResponse(
            {"error": "Category ID required"},
            status=400
        )
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    
    category.delete()
    return JsonResponse({}, status=204)