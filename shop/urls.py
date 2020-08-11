from django.contrib import admin
from django.urls import path
from . import views

app_name='shop'
urlpatterns = [
    path('', views.index,name='index'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('addcart/', views.updateCart,name='addcart'),
    path('process_order/', views.processOrder,name='process_order')
]
