import json
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from .models import Category

#Category views
def category_api(request, category_id=None):
    if request.method == "GET":
        if category_id is None:
            categories = Category.objects.all()
            data = [
                {"id": category.id, "name": category.name}
                for category in categories
            ]
            return JsonResponse(data, safe=False)
        else:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return JsonResponse({"error": "Not found"}, status=404)

            return JsonResponse({
                "id": category.id,
                "name": category.name
            })
    
    elif request.method == "POST":
        body = json.loads(request.body)
        category = Category.objects.create(
            name=body.get("name")
        )
        return JsonResponse({
            "id": category.id,
            "name": category.name
        }, status=201)

    elif request.method == "PUT":
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

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })
    
    elif request.method == "DELETE":
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

    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])

# Create your views here.
