from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Product, Couple, Gift_list, Gift_item


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="TestProduct", brand="TestBrand", price="100.00GBP", in_stock_quantity=1)

    def test_purchase(self):
        testProduct = Product.objects.get(name="TestProduct")
        self.assertEqual(testProduct.in_stock_quantity, 1)
        testProduct.buy()
        self.assertEqual(testProduct.in_stock_quantity, 0)
        self.assertRaises(ValidationError, testProduct.buy)


class GiftTestCase(TestCase):
    def setUp(self):
        product = Product.objects.create(name="TestProduct", brand="TestBrand", price="100.00GBP", in_stock_quantity=1)
        product2 = Product.objects.create(name="TestProduct2", brand="TestBrand", price="1.00GBP", in_stock_quantity=100)
        couple = Couple.objects.create(
            login_name="Couple"
            , login_password="Password"
            , groom_name="Test Groom"
            , bride_name="Test Bride"
            , email="test@test.com"
            , phone_number="+44 1632 960917"
        )
        gift_list = Gift_list.objects.create(name="Test list", couple=couple)
        Gift_item.objects.create(quantity=2, gift_list=gift_list, product=product, note="oos_test")
        Gift_item.objects.create(quantity=1, gift_list=gift_list, product=product2, note="more_test")
        Gift_item.objects.create(quantity=1, gift_list=gift_list, product=product2, note="quantity_test")

    def test_purchase_more(self):
        gift = Gift_item.objects.get(note="more_test")
        self.assertEqual(gift.bought_quantity, 0)
        self.assertEqual(gift.quantity, 1)
        gift.buy_one()
        self.assertEqual(gift.bought_quantity, 1)
        self.assertRaises(ValidationError, gift.buy_one)
        self.assertEqual(gift.bought_quantity, 1)

    def test_purchase_oos(self):
        gift = Gift_item.objects.get(note="oos_test")
        self.assertEqual(gift.bought_quantity, 0)
        self.assertEqual(gift.quantity, 2)
        gift.buy_one()
        self.assertEqual(gift.bought_quantity, 1)
        self.assertRaises(ValidationError, gift.buy_one)
        self.assertEqual(gift.bought_quantity, 1)

    def test_modify_quantity(self):
        gift = Gift_item.objects.get(note="quantity_test")
        self.assertEqual(gift.quantity, 1)
        self.assertRaises(ValidationError, gift.decrease_quantity)
        self.assertEqual(gift.quantity, 1)
        gift.increase_quantity()
        self.assertEqual(gift.quantity, 2)
