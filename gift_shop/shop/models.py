from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    in_stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)

class Gift(models.Model):
    groom_name = models.CharField(max_length=100, default="Andy Groom")
    bride_name = models.CharField(max_length=100, default="Beatrix Kiddo")
    added = models.DateTimeField(auto_now_add=True, editable=False)
    bought = models.BooleanField(default=False)
    product = models.ForeignKey(Product, related_name="gifts", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.groom_name + ' & ' + self.bride_name)
