from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creating user database"

    def handle(self, *args, **kwargs):  # allows to have a variable number of arguments
        users_to_create = [
            {
                "email": "alice@example.com",
                "password": "password123",
                "username": "Alice",
            },
            {"email": "bob@example.com", "password": "password123", "username": "Bob"},
            {
                "email": "charlie@example.com",
                "password": "password123",
                "username": "Charlie",
            },
            {
                "email": "sara@example.com",
                "password": "password123",
                "username": "Sara",
            },
            {"email": "leo@example.com", "password": "password123", "username": "Leo"},
        ]

        count = 0
        for data in users_to_create:
            if not User.objects.filter(email=data["email"]).exists():
                User.objects.create_user(
                    email=data["email"],
                    password=data["password"],
                    username=data["username"],
                )
                count += 1
                self.stdout.write(f"User {data['email']} created.")
            else:
                self.stdout.write(
                    self.style.WARNING(f"User {data['email']} already exists.")
                )

        if count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"{count} users created with success.")
            )
        else:
            self.stdout.write(self.style.NOTICE("No new user created."))
