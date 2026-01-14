from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product
from categories.models import Category
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create 20 products'

    def handle(self, *args, **kwargs):
        #User for 'created_by'
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()

        #Category creation
        cat_names = ['Pulls', 'Layette', 'Accessoires pour poupons']
        categories = {}
        for name in cat_names:
            cat, created = Category.objects.get_or_create(name=name)
            categories[name] = cat

        #Title list
        data_map = {
            'Pulls': ['Pull en laine torsadé', 'Petit pull marin', 'Gilet à boutons', 'Pull col roulé doudou'],
            'Layette': ['Brassière de naissance', 'Chaussons tricotés', 'Bonnet de naissance', 'Combinaison douce'],
            'Accessoires pour poupons': ['Mini couverture', 'Petit sac à langer', 'Béguin en coton', 'Écharpe miniature']
        }

        # 4. Generating 20 products
        count = 0
        for i in range(20):
            #Pick a category
            category_name = random.choice(cat_names)
            category_obj = categories[category_name]
            
            #Pick a name and add increment
            base_title = random.choice(data_map[category_name])
            full_title = f"{base_title} n°{i+1}"

            Product.objects.create(
                title=full_title,
                description=f"Ceci est une description détaillée pour le produit {full_title}. Fait main avec amour.",
                category=category_obj,
                created_by=admin_user
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Success : {count} products created !"))