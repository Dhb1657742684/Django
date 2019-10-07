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

from django.urls import path, re_path
from Seller.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('loginout/', loginout),
    path('send_login_code/', send_login_code),
    path('goods_add/', goods_add),
    # path('personal_info/', personal_info),
    re_path('cogs/(?P<oid>\d+)/', change_order_goods_status),
    re_path('goods_list/(?P<status>\d)/(?P<page>\d+)/', goods_list),
    re_path('order_list/(?P<status>\d)/(?P<page>\d+)/', order_list),
    re_path('change_status/(?P<st>\w+)/(?P<id>\d+)/', change_status),
]
