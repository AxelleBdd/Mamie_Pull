import json

from django.http import HttpResponseNotAllowed
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


@extend_schema(responses=CategorySerializer)
@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([AllowAny])
def category_api(request, category_id=None):
    if request.method == "GET":
        if category_id is None:
            return get_categories()
        else:
            return get_category(category_id)

    elif request.method == "POST":
        if not request.user.is_staff:
            return Response({"error": "Admin permission required"}, status=403)
        return create_category(request)

    elif request.method == "PUT":
        if not request.user.is_staff:
            return Response({"error": "Admin permission required"}, status=403)
        return update_category(request, category_id)

    elif request.method == "DELETE":
        if not request.user.is_staff:
            return Response({"error": "Admin permission required"}, status=403)
        return delete_category(category_id)

    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])


# GET all categories
def get_categories():
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# GET category by id
def get_category(category_id):
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# POST category
def create_category(request):
    body = json.loads(request.body)
    category = Category.objects.create(name=body.get("name"))
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=201)


# PUT category
def update_category(request, category_id):
    if category_id is None:
        return Response({"error": "Category ID required"}, status=400)
    body = json.loads(request.body)
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    category.name = body.get("name", category.name)
    category.save()
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=201)


# DELETE category
def delete_category(category_id):
    if category_id is None:
        return Response({"error": "Category ID required"}, status=400)
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    category.delete()
    return Response({}, status=204)
