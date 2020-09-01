import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gift_shop.settings')

import django
django.setup()

import json
from shop.models import Product, Couple, Gift_list

from django.contrib.auth.models import User

def populate():
    with open("products.json") as json_file:
        data = json.load(json_file)
        for product in data:
            name = product["name"]
            brand = product["brand"]
            price = product["price"]
            in_stock_quantity = int(product["in_stock_quantity"])
            Product.objects.get_or_create(name=name, brand=brand, price=price, in_stock_quantity=in_stock_quantity)


def add_dummy_couple_and_gift_list():
    user = User.objects.create_user('testCouple', 'shared_email@ymail.com', 'password')
    user.couple.groom_name = "Andy Groom"
    user.couple.bride_name = "Beatrix Kiddo"
    user.couple.phone_number = "+44 1632 960917"
    user.save()

    name = "Dummy Gift List"
    Gift_list.objects.get_or_create(name=name, couple=user.couple)


populate()
add_dummy_couple_and_gift_list()
