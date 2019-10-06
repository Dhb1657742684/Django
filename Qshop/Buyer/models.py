from django.db import models
from Seller.views import User


class GoodsType(models.Model):
    type_label = models.CharField(max_length=32)
    type_desc = models.TextField()
    type_photo = models.ImageField(upload_to='foreground/images', default='images/banner01.jpg')


class Goods(models.Model):
    goods_num = models.CharField(max_length=11, null=True, blank=True)  # 商品编号
    goods_name = models.CharField(max_length=32, null=True, blank=True)  # 商品名称
    goods_price = models.FloatField(null=True, blank=True)  # 价格
    goods_price_data = models.DateField(auto_now=True)  # 生产日期
    goods_inven = models.IntegerField(null=True, blank=True)  # 库存
    goods_area = models.CharField(max_length=32, null=True, blank=True)  # 产地
    goods_expr = models.IntegerField(null=True, blank=True)  # 保质期
    goods_status = models.IntegerField(default=1)  # 状态 0为下架商品 1为在售商品
    goods_photo = models.ImageField(upload_to='foreground/image', default='image/defaule_img.jpg')
    goods_user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    goods_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE, default=1)


class PayOrder(models.Model):
    order_num = models.CharField(max_length=32)  # 订单编号
    order_date = models.DateTimeField(auto_now=True)  # 订单时间
    order_status = models.IntegerField()  # 订单状态 0 未支付 1 已支付 2 待收货 3 完成 4 拒收
    order_total = models.FloatField(blank=True, null=True)  # 订单总价
    order_user = models.ForeignKey(to=User, on_delete=models.CASCADE)  # 订单用户


class OrderInfo(models.Model):
    order_id = models.ForeignKey(to=PayOrder, on_delete=models.CASCADE)  # 订单ID
    goods_id = models.IntegerField()  # 商品ID
    goods_photo = models.CharField(max_length=32)  # 商品照片
    goods_name = models.CharField(max_length=32)  # 商品名称
    goods_count = models.IntegerField()  # 商品总数
    goods_price = models.FloatField()  # 商品单价
    goods_total = models.FloatField()  # 商品总价
    goods_status = models.IntegerField(default=0)  # 商品状态 0 未支付 1 已支付 2 待收货 3 完成 4 拒收
    store_id = models.ForeignKey(to=User, on_delete=models.CASCADE)  # 商店ID


class Cart(models.Model):
    goods_name = models.CharField(max_length=32)
    goods_num = models.IntegerField()
    goods_price = models.FloatField()
    goods_photo = models.CharField(max_length=32)
    goods_total = models.FloatField()
    goods_id = models.IntegerField()
    cart_user = models.IntegerField()
# Create your models here.
