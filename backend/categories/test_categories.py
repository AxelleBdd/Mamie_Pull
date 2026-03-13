from django.test import TestCase
from products.models import Category
from categories.models import Category

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Test Category 1")
        Category.objects.create(name="Test Category 2")

    # POST
    def test_category_creation(self):
        category1 = Category.objects.get(name="Test Category 1")
        category2 = Category.objects.get(name="Test Category 2")
        self.assertEqual(category1.name, "Test Category 1")
        self.assertEqual(category2.name, "Test Category 2")

    # GET (all, by id)
    def test_category_get_all(self):
        categories = Category.objects.all()
        self.assertEqual(len(categories), 2)

    def test_category_get_category_by_id(self):
        category = Category.objects.get(name="Test Category 1")
        self.assertEqual(category.name, "Test Category 1")

    # PUT
    def test_category_update(self):
        category = Category.objects.get(name="Test Category 1")
        category.name = "Updated Test Category 1"
        category.save()
        updated_category = Category.objects.get(id=category.id)
        self.assertEqual(updated_category.name, "Updated Test Category 1")

    # DELETE
    def test_category_delete(self):
        category = Category.objects.get(name="Test Category 1")
        category.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name="Test Category 1")