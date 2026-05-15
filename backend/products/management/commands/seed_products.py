import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from categories.models import Category
from products.models import Product

User = get_user_model()


class Command(BaseCommand):
    help = "Create 20 products"

    def handle(self, *args, **kwargs):
        # User for 'created_by'
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()

        # Category creation
        cat_names = ["Pulls", "Layette", "Accessoires pour poupons"]
        categories = {}
        for name in cat_names:
            cat, created = Category.objects.get_or_create(
                name=name, defaults={"slug": slugify(name)}
            )
            if not cat.slug:
                cat.slug = slugify(name)
                cat.save()

            categories[name] = cat

        # Title list
        data_map = {
            "Pulls": [
                "Pull en laine torsadé",
                "Petit pull marin",
                "Gilet à boutons",
                "Pull col roulé doudou",
            ],
            "Layette": [
                "Brassière de naissance",
                "Chaussons tricotés",
                "Bonnet de naissance",
                "Combinaison douce",
            ],
            "Accessoires pour poupons": [
                "Mini couverture",
                "Petit sac à langer",
                "Écharpe miniature",
            ],
        }

        # Sizes for each category
        sizes_map = {
            "Pulls": ["3 mois", "6 mois", "12 mois", "18 mois", "24 mois", "36 mois"],
            "Layette": ["Naissance", "3 mois", "6 mois"],
            "Accessoires pour poupons": ["Taille unique"],
        }

        # 4. Generating 20 products
        count = 0
        for i in range(20):
            # Pick a category
            category_name = random.choice(cat_names)
            category_obj = categories[category_name]

            # Pick a name
            base_title = random.choice(data_map[category_name])

            # Check if base_title already exists
            if Product.objects.filter(title=base_title).exists():
                # Find the next available increment starting from 2
                increment = 2
                while Product.objects.filter(
                    title=f"{base_title} n°{increment}"
                ).exists():
                    increment += 1
                full_title = f"{base_title} n°{increment}"
            else:
                full_title = base_title

            # Get sizes for the category
            available_sizes = sizes_map[category_name]

            Product.objects.create(
                title=full_title,
                description=f"Ceci est une description pour le produit {full_title}.",
                category=category_obj,
                sizes=available_sizes,
                created_by=admin_user,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Success : {count} products created !"))
