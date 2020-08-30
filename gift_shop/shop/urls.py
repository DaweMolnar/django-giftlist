from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('gifts/', views.GiftListView.as_view(), name='gifts'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
]
