from django.test import TestCase

from products.models import Category, Product


class ProductTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Test Category")
        Product.objects.create(
            title="Test Product 1",
            description="Description for product 1",
            category=category,
            sizes=["18 mois", "24 mois", "36 mois"],
        )
        Product.objects.create(
            title="Test Product 2",
            description="Description for product 2",
            category=category,
            sizes=["One size"],
        )

    # POST
    def test_product_creation(self):
        product1 = Product.objects.get(title="Test Product 1")
        product2 = Product.objects.get(title="Test Product 2")
        self.assertEqual(product1.description, "Description for product 1")
        self.assertEqual(product2.description, "Description for product 2")
        self.assertEqual(product1.sizes, ["18 mois", "24 mois", "36 mois"])
        self.assertEqual(product2.sizes, ["One size"])

    # GET (all, by id, by category)
    def test_product_get_all(self):
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

    def test_product_get_product_by_id(self):
        product = Product.objects.get(title="Test Product 1")
        self.assertEqual(product.description, "Description for product 1")

    def test_product_get_products_by_category(self):
        category = Category.objects.get(name="Test Category")
        products = Product.objects.filter(category=category)
        self.assertEqual(len(products), 2)

    # PUT
    def test_product_update(self):
        product = Product.objects.get(title="Test Product 1")
        product.description = "Updated description for product 1"
        product.save()
        updated_product = Product.objects.get(title="Test Product 1")
        self.assertEqual(
            updated_product.description, "Updated description for product 1"
        )

    # DELETE
    def test_product_delete(self):
        product = Product.objects.get(title="Test Product 1")
        product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(title="Test Product 1")
