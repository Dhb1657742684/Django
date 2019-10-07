"""Qshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Buyer.views import *
from django.urls import path,re_path

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('pay/', pay),
    path('shop_car/', shop_cart),
    path('index/', index),
    re_path('detail/(?P<id>\d+)/', detail),
    path('loginout/', loginout),
    # path('user_info/', user_info),
    path('add_cart/', add_cart),
    path('pay_order/', pay_order),
    path('order_result/', order_result),
    path('user_center_order/', user_center_order),
    re_path('goods_list/(?P<page>\d+)/?', goods_list),
]
