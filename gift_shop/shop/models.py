from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    in_stock_quantity = models.PositiveIntegerField(default=0)

    def buy(self):
        if self.in_stock_quantity == 0:
            raise ValidationError("Cannot buy products that are not in stock")
        self.in_stock_quantity -= 1
        self.save()

    def __str__(self):
        return str(self.name)


class Couple(models.Model):
    login_name = models.CharField(max_length=50)
    login_password = models.CharField(max_length=256)
    groom_name = models.CharField(max_length=100, default="Andy Groom")
    bride_name = models.CharField(max_length=100, default="Beatrix Kiddo")
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return str(self.login_name)


class Gift_list(models.Model):
    name = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    couple = models.ForeignKey(Couple, related_name="gift_lists", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Gift_item(models.Model):
    added = models.DateTimeField(auto_now_add=True, editable=False)
    bought_quantity = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=500)
    gift_list = models.ForeignKey(Gift_list, related_name="gifts", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="gifts", on_delete=models.CASCADE)

    def buy_one(self):
        if self.bought_quantity == self.quantity:
            raise ValidationError("Cannot buy more gift then needed!")
        self.product.buy()
        self.bought_quantity += 1
        self.save()

    def increase_quantity(self):
        self.quantity += 1
        self.save()

    def decrease_quantity(self):
        self.quantity -= 1
        self.save()

    def __str__(self):
        return str(self.product.name)