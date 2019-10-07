import hashlib
import random
import time
import datetime
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from Seller.models import *
from Buyer.models import *
from alipay import AliPay
from django.http import JsonResponse
from django.core.paginator import Paginator


# 返回页码的方法
def back_page(pages, current_page):  # pages 总页数  step 当前页数
    if pages <= 5:
        return range(1, pages + 1)
    if 0 <= current_page <= pages:
        if current_page <= 3:
            return [1, 2, 3, 4, 5]
        elif current_page >= pages - 2:
            return [pages - 4, pages - 3, pages - 2, pages - 1, pages]
        else:
            return [current_page - 2, current_page - 1, current_page, current_page + 1, current_page + 2]


def loginVaild(fun):
    def inner(request, *args, **kwargs):
        coo_email = request.COOKIES.get('email')
        sess_email = request.session.get('email')
        if coo_email and sess_email:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/ForeGround/login/')

    return inner


def detail(request, id):
    id = int(id)
    goods = Goods.objects.filter(id=id).first()
    return render(request, 'buyer/detail.html', locals())


# 密码加密
def set_pwd(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result


def loginValid(fun):  # 登录校验
    def inner(request, *args, **kwargs):
        email = request.COOKIES.get('email')
        id = request.COOKIES.get('user_id')
        se_email = request.session.get('email')
        if email and se_email and email == se_email:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Buyer/login/')

    return inner


def register(request):  # 注册
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        if email:
            if username:
                if pwd and cpwd and pwd == cpwd:
                    db = User.objects.filter(email=email).first()
                    if not db:
                        user = User()
                        user.username = username
                        user.email = email
                        user.password = set_pwd(pwd)
                    else:
                        err_msg = '该账号已注册'
                else:
                    err_msg = '两次输入密码不同'
            else:
                err_msg = '用户名不可为空'
        else:
            err_msg = '邮箱不可为空'
    return render(request, 'buyer/register.html', locals())


def login(request):  # 注册
    err_msg = ''
    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        if email:
            db = User.objects.filter(email=email).first()
            if db:
                if db.password == set_pwd(pwd):
                    response = HttpResponseRedirect('/Buyer/index/')
                    response.set_cookie('email', db.email)
                    response.set_cookie('user_id', db.id)
                    request.session['email'] = db.email
                    return response
                else:
                    err_msg = '密码错误'
            else:
                err_msg = '该账号未注册'
        else:
            err_msg = '邮箱不可为空'
    return render(request, 'buyer/login.html', locals())


# 退出
def loginout(request):
    response = HttpResponseRedirect('/ForeGround/index/')  # 回到登录页
    cookies = request.COOKIES.keys()
    for key in cookies:  # 删除cookie和session
        response.delete_cookie(key)
    del request.session['email']
    return response


@loginValid
def index(request):
    email = request.COOKIES.get('email')
    if email:
        user = User.objects.get(email=email)
    gts = GoodsType.objects.all()
    data = {}
    for gt in gts:
        datas = gt.goods_set.all()
        if len(datas) >= 4:
            datas = datas[0:4]
            data.setdefault(gt, datas)
    return render(request, 'buyer/index.html', locals())


def goods_add(request):
    goods_names = '毛巾、杯子、水桶、筛子、垃圾桶、脚凳、手套、安全帽、工作服、笔记本、笔、文件夹、文具袋、名片盒、毛公仔、变形金刚、西红柿、南瓜、生菜、玉米、韭菜、卷心菜、萝卜、白菜、黄瓜、胡萝卜、大蒜、葱、木耳、豌豆、马铃薯、芋、苦瓜、洋葱、芹菜、地瓜、蘑菇、橄榄、菠菜、冬瓜、莲藕、紫菜、油菜、茄子、香菜、青椒、银耳、牛蒡、竹笋、绿豆、毛豆、豆芽菜'
    g_lst = goods_names.split('、')
    goods_area = '北京，天津，上海，重庆，河北，山西，辽宁，吉林，黑龙江，江苏，浙江，安徽，福建，江西，山东，河南，湖北，湖南，广东，海南，四川，贵州，云南，陕西，甘肃，青海，台湾，内蒙古，广西，西藏，宁夏，新疆，香港，澳门'
    g_area = goods_area.split('，')
    for i in range(100):
        goods = Goods()
        goods.goods_name = str(i + 1).zfill(5)
        goods.goods_num = random.choice(g_lst)
        goods.goods_price = round(random.random() * 100, 2)
        goods.goods_inven = random.randint(20, 100)
        goods.goods_area = random.choice(g_area)
        goods.goods_expr = random.randint(1, 24)
        # goods.save()
    return HttpResponse('hello world')


def goods_list(request, page):
    page = int(page)
    page_size = 10
    type = request.GET.get('type')
    keyword = request.GET.get('keyword')
    goods_lst = []
    if type:
        gt = GoodsType.objects.get(type_label=type)
        goods_lst = gt.goods_set.all()
    elif keyword:
        goods_lst = Goods.objects.filter(goods_num__contains=keyword)
    if goods_lst:
        get_page = Paginator(goods_lst, 10)
        goods_list = get_page.page(page)
        bp = back_page(get_page.num_pages, page)
        if page == 1:
            b_p = 1
        else:
            b_p = page - 1
        if page == get_page.num_pages:
            a_p = get_page.num_pages
        else:
            a_p = page + 1
    if len(goods_lst) <= 5:
        recomm_goods = Goods.objects.order_by('-goods_price_data')[:1]
    else:
        recomm_goods = Goods.objects.order_by('-goods_price_data')[:2]
    return render(request, 'buyer/goods_list.html', locals())


# 支付宝支付
from Qshop.settings import alipay_public_key_string, alipay_private_key_string


def pay(request):
    order_num = request.GET.get('order_num')
    order = PayOrder.objects.get(order_num=order_num)
    alipay = AliPay(
        appid='2016101200667717',
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2'
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_num,
        total_amount=str(order.order_total),
        subject='生鲜交易',
        return_url='http://127.0.0.1:8000/ForeGround/order_result/',
        notify_url='http://127.0.0.1:8000/ForeGround/order_result/'
    )
    result = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return HttpResponseRedirect(result)


# 支付结果
def order_result(request):
    order_num = request.GET.get('out_trade_no')
    order = PayOrder.objects.get(order_num=order_num)
    order.order_status = 1
    order.orderinfo_set.all().update(goods_status=1)
    order.save()
    return render(request, 'buyer/order_result.html')


# 加入购物车
@loginVaild
def add_cart(request):
    result = {
        'code': 200,
        'data': ''
    }
    if request.method == 'POST':
        id = int(request.POST.get('goods_id'))
        count = int(request.POST.get('count', 1))
        goods = Goods.objects.get(id=id)
        cart = Cart()
        cart.goods_name = goods.goods_num
        cart.goods_num = count
        cart.goods_price = goods.goods_price
        cart.goods_photo = goods.goods_photo
        cart.goods_total = round(goods.goods_price * count, 2)
        cart.goods_id = id
        cart.cart_user = request.COOKIES.get('user_id')
        cart.save()
        result['data'] = '加入成功'
    else:
        result['code'] = 500
        result['data'] = '请求方式错误'
    return JsonResponse(result)


# 购物车
@loginVaild
def shop_cart(request):
    user_id = request.COOKIES.get('user_id')
    total = 0
    goods = Cart.objects.filter(cart_user=int(user_id)).order_by('-id')
    for good in goods:
        total += good.goods_total
    count = goods.count()
    return render(request, 'buyer/shop_cart.html', locals())


@loginVaild
def pay_order(request):
    datas = request.GET
    d = []
    goods_id = request.GET.getlist('goods_id')
    goods_count = request.GET.getlist('count')
    n = len(goods_id)
    for i in range(n):
        d.append((goods_id[i], goods_count[i]))
    if goods_id and goods_count:
        order = PayOrder()  # 实例化订单
        order.order_num = str(time.time()).replace('.', '')  # 订单编号
        order.order_date = datetime.datetime.now()  # 订单时间
        order.order_status = 0  # 订单状态
        id = int(request.COOKIES.get('user_id'))
        order.order_user = User.objects.get(id=id)  # 订单用户
        order.save()
        total = 0
        for i in d:
            goods = Goods.objects.get(id=int(i[0]))
            order_info = OrderInfo()
            order_info.order_id = order
            order_info.goods_id = i[0]
            order_info.goods_photo = goods.goods_photo
            order_info.goods_name = goods.goods_num
            order_info.goods_count = int(i[1])
            order_info.goods_price = goods.goods_price
            order_info.goods_total = goods.goods_price * int(i[1])
            order_info.goods_status = 0
            total += goods.goods_price * int(i[1])
            order_info.store_id = goods.goods_user
            order_info.save()
        order.order_total = total
        order.save()
    return render(request, 'buyer/pay_order.html', locals())


def user_center_order(request):
    id = request.COOKIES.get('user_id')
    orders = PayOrder.objects.filter(order_user=id).order_by('-order_date')
    return render(request, 'buyer/user_center_order.html', locals())
# Create your views here.
