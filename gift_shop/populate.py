import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gift_shop.settings')

import django
django.setup()

import json
from shop.models import Product, Couple, Gift_list


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
    login_name = "Couple"
    login_password = "InsecurePassword"
    groom_name = "Andy Groom"
    bride_name = "Beatrix Kiddo"
    email = "shared_email@ymail.com"
    phone_number = "+44 1632 960917"
    Couple.objects.get_or_create(
        login_name=login_name
        , login_password=login_password
        , groom_name=groom_name
        , bride_name=bride_name
        , email=email
        , phone_number=phone_number
    )
    name = "Dummy Gift List"
    Gift_list.objects.get_or_create(name=name, couple=Couple.objects.all().first())


populate()
add_dummy_couple_and_gift_list()
