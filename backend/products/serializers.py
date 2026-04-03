from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # Display category name instead of id
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_name",
            "image",
            "sizes",
            "created_by",
        ]
