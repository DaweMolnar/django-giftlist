from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from . import models
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'shop/index.html'


class ProductListView(ListView):
    model = models.Product

    def get_queryset(self):
        if self.request.method == 'GET':
            product_id = self.request.GET.get('product_id', None)
            if product_id is not None:
                self.add_product(product_id)
        return models.Product.objects.all()

    def add_product(self, product_id):
        product = models.Product.objects.get(pk=product_id)
        gift_list = models.Gift_list.objects.all().first()  # TODO handle multiple lists
        gift, created = models.Gift_item.objects.get_or_create(gift_list=gift_list, product=product)
        if not created:
            gift.increase_quantity()
        messages.info(self.request, "Successfully added gift to gift list")


class ProductDetailView(DetailView):
    context_object_name = 'product_details'
    model = models.Product
    template_name = 'shop/product_detail.html'


class GiftListView(ListView):
    context_object_name = 'gift_lists'
    template_name = 'shop/gift_list.html'
    model = models.Gift_list

    def get_queryset(self):
        if self.request.method == 'GET':
            delete_gift_id = self.request.GET.get('delete_gift_id', None)
            buy_gift_id = self.request.GET.get('buy_gift_id', None)
            if delete_gift_id is not None:  # TODO handle delete if one gift was already bougth
                self.delete_gift(delete_gift_id)
            if buy_gift_id is not None:
                self.buy_gift(buy_gift_id)
        return models.Gift_list.objects.all()

    def delete_gift(self, gift_id):
        try:
            gift = models.Gift_item.objects.get(pk=gift_id)
            if gift.quantity == 1:
                gift.delete()
            else:
                gift.decrease_quantity()
            messages.info(self.request, "Successfully removed a gift")
        except ValidationError as err:
            messages.error("Error when deleting gift: {}".format(err))

    def buy_gift(self, gift_id):
        try:
            gift = models.Gift_item.objects.get(pk=gift_id)
            gift.buy_one()
            messages.info(self.request, "Successfully bought gift")
        except ValidationError as err:
            messages.error(self.request, "Error when buying gift: {}".format(err))


class ReportView(ListView):
    model = models.Gift_list
    context_object_name = 'reports'
    template_name = 'shop/report.html'


class LoginView(View):
    template_name = 'shop/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
            else:
                messages.error(self.request, "Inactive user.")
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(self.request, "Invalid login details supplied")
        return HttpResponseRedirect(reverse('shop:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
