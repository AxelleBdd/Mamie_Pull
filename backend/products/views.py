import json
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render

from products.models import Product

#Products views
def product_api(request, product_id=None):
    if request.method == 'GET' :
        if product_id is None: #GET all
            products = Product.objects.all()
            data = [
                {"id": product.id, "title": product.title, "description": product.description, "category": product.category, "image": product.image}
                for product in products
            ]
            return JsonResponse(data, safe=False)
        else:
            try: #GET product_id
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
        
    elif request.method == "POST":
        body = json.loads(request.body)
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
    
    elif request.method == "PUT":
        if product_id is None:
            return JsonResponse(
                {"error": "Product ID required"},
                status=400
            )

        body = json.loads(request.body)
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
    
    elif request.method == "DELETE":
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

    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])

