from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser1", email="testuser1@example.com", password="testpass1")
        User.objects.create_user(username="testuser2", email="testuser2@example.com", password="testpass2")
    
    # POST
    def test_user_creation(self):
        user1 = User.objects.get(username="testuser1")
        user2 = User.objects.get(username="testuser2")
        self.assertEqual(user1.email, "testuser1@example.com")
        self.assertEqual(user2.email, "testuser2@example.com")
    
    #PUT
    def test_user_update(self):
        user1 = User.objects.get(username="testuser1")
        user1.email = "updated@example.com"
        user1.save()
        updated_user1 = User.objects.get(username="testuser1")
        self.assertEqual(updated_user1.email, "updated@example.com")

    #DELETE
    def test_user_deletion(self):
        user2 = User.objects.get(username="testuser2")
        user2.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="testuser2")
    