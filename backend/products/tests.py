from django.test import TestCase
from products.models import Product
from products.models import Category

# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Test Category")
        Product.objects.create(title="Test Product 1", description="Description for product 1", category_id=1)
        Product.objects.create(title="Test Product 2", description="Description for product 2", category_id=1)

    def test_product_creation(self):
        product1 = Product.objects.get(title="Test Product 1")
        product2 = Product.objects.get(title="Test Product 2")
        self.assertEqual(product1.description, "Description for product 1")
        self.assertEqual(product2.description, "Description for product 2")
