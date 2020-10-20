from django.contrib import admin
from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products_detail/<slug:slug>', views.product_detail, name = 'product_detail'),
    path('<slug:slug>/bid', views.product_bid, name = 'product_bid'),
    path('<slug:slug>/product_remove', views.product_delete, name = 'product_delete'),
    path('<int:bid>/<int:num>/bid/', views.products_status, name= 'product_status'),
    path('search/', views.search, name='search')

]

