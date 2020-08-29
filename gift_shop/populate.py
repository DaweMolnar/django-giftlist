import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gift_shop.settings')

import django
django.setup()

import json
from shop.models import Product


def populate():
    with open("products.json") as json_file:
        data = json.load(json_file)
        for product in data:
            name = product["name"]
            brand = product["brand"]
            price = product["price"]
            in_stock_quantity = int(product["in_stock_quantity"])
            Product.objects.get_or_create(name=name, brand=brand, price=price, in_stock_quantity=in_stock_quantity)

populate()