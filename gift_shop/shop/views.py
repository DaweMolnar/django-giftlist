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


class ProductDetailView(DetailView):
    context_object_name = 'product_details'
    model = models.Product
    template_name = 'shop/product_detail.html'