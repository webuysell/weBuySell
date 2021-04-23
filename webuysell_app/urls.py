from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('product/<int:product_id>', views.product),
    path('add_product', views.add_product),
]