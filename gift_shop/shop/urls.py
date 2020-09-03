from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'shop'

urlpatterns = [
    path('', login_required(views.ProductListView.as_view()), name='list'),
    path('gifts/', views.GiftListView.as_view(), name='gifts'),
    path('report/', login_required(views.ReportView.as_view()), name='report'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
