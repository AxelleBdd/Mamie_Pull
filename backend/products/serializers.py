from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # Display category name instead of id
    category_name = serializers.ReadOnlyField(source="category.name")
    # Display created_by user email
    created_by_name = serializers.CharField(source="created_by.email", read_only=True)

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
            "created_by_name",
        ]
        read_only_fields = ["id", "created_by", "created_by_name"]
