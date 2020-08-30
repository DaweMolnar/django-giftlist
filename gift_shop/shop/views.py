from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from . import models
# Create your views here.


class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'shop/index.html'


class ProductListView(ListView):
    model = models.Product

    def get_queryset(self):
        if self.request.method == 'GET':
            product_id = self.request.GET.get('product_id', None)
            if product_id != None:
                self.add_product(product_id)
        return models.Product.objects.all()

    def add_product(self, product_id):
        product = models.Product.objects.get(pk=product_id)
        gift_list = models.Gift_list.objects.all().first() #TODO handle multiple lists
        gift, created = models.Gift_item.objects.get_or_create(gift_list=gift_list, product=product)
        if not created:
            gift.increase_quantity()


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
            gift_id = self.request.GET.get('gift_id', None)
            if gift_id != None:
                gift = models.Gift_item.objects.get(pk=gift_id)
                if gift.quantity == 1:
                    gift.delete()
                else:
                    gift.decrease_quantity()
        return models.Gift_list.objects.all()
