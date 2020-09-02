from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from .models import Product, Gift_list, Gift_item
from .views import GiftListView, ProductListView, LoginView
from django.contrib.messages.storage.fallback import FallbackStorage


def mocked_message_request(request):
    """
    default messages doesn't work with RequestFactory
    :param request:
    :return:
    """
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    return request


def set_up_gifts():
    Product.objects.create(name="NotSelectedProduct", brand="TestBrand", price="100.00GBP", in_stock_quantity=1)
    product = Product.objects.create(name="TestProduct", brand="TestBrand", price="100.00GBP", in_stock_quantity=1)
    product2 = Product.objects.create(name="TestProduct2", brand="TestBrand", price="1.00GBP", in_stock_quantity=100)
    user = User.objects.create_user('Couple', 'test@test.com', 'password')
    user.couple.groom_name = "Test Groom"
    user.couple.bride_name = "Test Bride"
    user.couple.phone_number = "+44 1632 960917"
    user.save()
    gift_list = Gift_list.objects.create(name="Test list", couple=user.couple)
    Gift_item.objects.create(quantity=2, gift_list=gift_list, product=product, note="oos_test")
    Gift_item.objects.create(quantity=1, gift_list=gift_list, product=product2, note="more_test")
    Gift_item.objects.create(quantity=1, gift_list=gift_list, product=product2, note="quantity_test")


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
        set_up_gifts()

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
        gift.decrease_quantity()


class GiftViewTest(TestCase):

    def setUp(self):
        set_up_gifts()

    def set_up_view(self):
        request = RequestFactory().get('/')
        request = mocked_message_request(request)
        if not request.GET._mutable:
            request.GET._mutable = True
        view = GiftListView()
        view.setup(request)
        return view

    def test_gift_buy(self):
        gift = Gift_item.objects.get(note="more_test")
        view = self.set_up_view()
        self.assertEqual(gift.bought_quantity, 0)
        view.buy_gift(gift.id)
        gift = Gift_item.objects.get(note="more_test")
        self.assertEqual(gift.bought_quantity, 1)

    def test_gift_remove(self):
        gift = Gift_item.objects.get(note="more_test")
        view = self.set_up_view()
        self.assertEqual(gift.quantity, 1)
        view.delete_gift(gift.id)
        self.assertRaises(Gift_item.DoesNotExist, Gift_item.objects.get, note="more_test")
        gift = Gift_item.objects.get(note="oos_test")
        self.assertEqual(gift.quantity, 2)
        view.delete_gift(gift.id)
        gift = Gift_item.objects.get(note="oos_test")
        self.assertEqual(gift.quantity, 1)

    def test_query_remove(self):
        gift = Gift_item.objects.get(note="more_test")
        view = self.set_up_view()
        view.request.GET['delete_gift_id'] = str(gift.id)
        view.get_queryset()
        self.assertRaises(Gift_item.DoesNotExist, Gift_item.objects.get, note="more_test")

    def test_query_buy(self):
        gift = Gift_item.objects.get(note="more_test")
        view = self.set_up_view()
        view.request.GET['buy_gift_id'] = str(gift.id)
        view.get_queryset()
        gift = Gift_item.objects.get(note="more_test")
        self.assertEqual(gift.bought_quantity, 1)


class ProductViewTest(TestCase):

    def setUp(self):
        set_up_gifts()

    def set_up_view(self):
        request = RequestFactory().get('/')
        request = mocked_message_request(request)
        if not request.GET._mutable:
            request.GET._mutable = True
        view = ProductListView()
        view.setup(request)
        return view

    def test_product_add(self):
        test_product = Product.objects.get(name="NotSelectedProduct")
        view = self.set_up_view()
        self.assertEqual(len(test_product.gifts.all()), 0)
        view.request.GET['product_id'] = str(test_product.id)
        view.get_queryset()
        self.assertEqual(len(test_product.gifts.all()), 1)
        gift = test_product.gifts.all().first()
        self.assertEqual(gift.quantity, 1)
        view.get_queryset()
        gift = test_product.gifts.all().first()
        self.assertEqual(gift.quantity, 2)


class LoginViewTest(TestCase):
    def setUp(self):
        set_up_gifts()

    def set_up_view(self):
        request = RequestFactory().get('/')
        request = mocked_message_request(request)
        request.user = AnonymousUser()
        request.session = self.client.session
        request.session.create()
        if not request.POST._mutable:
            request.POST._mutable = True
        view = LoginView()
        view.setup(request)
        return view

    def test_login_correct(self):
        view = self.set_up_view()
        view.request.POST['username'] = "Couple"
        view.request.POST['password'] = "password"
        self.assertFalse(view.request.user.is_authenticated)
        view.post(view.request)
        self.assertTrue(view.request.user.is_authenticated)

    def test_login_incorrect(self):
        view = self.set_up_view()
        view.request.POST['username'] = "Couple"
        view.request.POST['password'] = "Wrongpassword"
        self.assertFalse(view.request.user.is_authenticated)
        view.post(view.request)
        self.assertFalse(view.request.user.is_authenticated)
