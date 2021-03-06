import time
import datetime
import random
from Buyer.views import back_page
from django.shortcuts import render, HttpResponseRedirect
from Seller.models import *
from Buyer.models import *
import hashlib
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


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
            return HttpResponseRedirect('/Seller/login/')

    return inner


# 返回验证码
def random_code(len=4):
    str1 = ''.join([str(i) for i in range(10)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)])
    code = ''.join([random.choice(str1) for i in range(len)])
    return code


# 生成并发送验证码
@csrf_exempt
def send_login_code(request):
    result = {
        'code': 200,
        'data': '',
        'random_code': ''
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        code = random_code()
        c = Valid_Code()
        c.code_user = email
        c.code_content = code
        c.save()
        send_data = '%s的验证码是【%s】，不要让别人知道啊' % (email, code)
        result['data'] = '发送成功'
        result['random_code'] = code
    else:
        result['code'] = 400
        result['data'] = '请求错误'
    return JsonResponse(result)


def register(request):  # 注册功能
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            if username:
                if password:
                    db = User.objects.filter(email=email).first()
                    if not db:
                        user = User()
                        user.username = username
                        user.email = email
                        user.password = set_pwd(password)
                        user.save()
                    else:
                        err_msg = '该账号已注册'
                else:
                    err_msg = '密码不可为空'
            else:
                err_msg = '用户名不可为空'
        else:
            err_msg = '邮箱不可为空'
    return render(request, 'seller/register.html', locals())


def login(request):  # 登录功能
    err_msg = ''
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        code = request.POST.get("code")
        if email:  # 判断邮箱是否为空
            db_user = User.objects.filter(email=email).first()
            password = set_pwd(password)  # 获取页面输入的密码
            if db_user:  # 判断账号是否存在
                if password == db_user.password:  # 判断密码是否正确
                    codes = Valid_Code.objects.filter(code_user=email).order_by("-code_time").first()
                    # 校验验证码是否存在，是否过期，是否被使用
                    now = time.mktime(datetime.datetime.now().timetuple())  # 把当前时间转换为时间戳
                    db_time = time.mktime(codes.code_time.timetuple())  # 把数据库内的时间转换为时间戳
                    t = (now - db_time) / 60
                    if codes and codes.code_status == 0 and t <= 5 and codes.code_content.upper() == code.upper():
                        response = HttpResponseRedirect('/Seller/index/')  # 跳转页面
                        response.set_cookie('email', email)  # 设置cookie
                        response.set_cookie('user_id', db_user.id)
                        request.session['email'] = db_user.email  # 设置session
                        codes.code_status = 1
                        codes.save()
                        return response
                    else:
                        err_msg = '验证码错误'
                else:
                    err_msg = '密码错误'
            else:
                err_msg = '该邮箱不存在'
        else:
            err_msg = '邮箱不能为空'
    return render(request, 'seller/login.html', locals())


def loginout(request):  # 退出登录
    response = HttpResponseRedirect('/Seller/login/')  # 回到登录页
    cookies = request.COOKIES.keys()
    for key in cookies:  # 删除cookie和session
        response.delete_cookie(key)
    del request.session['email']
    return response


@loginValid
def index(request):
    return render(request, 'seller/index.html')


@loginValid
def goods_list(request, status, page=1):
    email = request.COOKIES.get('email')
    user = User.objects.filter(email=email).first()
    static = int(status)
    page = int(page)
    next_page = page + 1
    page_size = 10
    if static == 1:
        good_lst = Goods.objects.filter(goods_status=1)
    elif static == 0:
        good_lst = Goods.objects.filter(goods_status=0)
    else:
        good_lst = Goods.objects.all()
    gd_list = Paginator(good_lst, page_size)  # 进行分页
    goods = gd_list.page(page)  # 返回对应页的数据
    pages = gd_list.num_pages  # 获取总页数
    bapa = back_page(pages, page)
    return render(request, 'seller/goods_list.html', locals())


@loginValid
def order_list(request, status, page=1):  # 订单列表
    status = int(status)
    page = int(page)
    email = request.COOKIES.get('email')
    store = User.objects.get(email=email)  # 获取店铺信息
    orders = store.orderinfo_set.filter(goods_status=status).order_by("-id")  # 获取店铺对应的订单
    return render(request, 'seller/order_list.html', locals())


def goods_add(request):
    email = request.COOKIES.get('email')
    user = User.objects.filter(email=email).first()
    goods_type = GoodsType.objects.all()
    if request.method == 'POST':
        cook = request.COOKIES.get('email')
        user = User.objects.get(email=email)
        goods = Goods()
        goods.goods_num = request.POST.get('goods_num')
        goods.goods_name = request.POST.get('goods_name')
        goods.goods_price = request.POST.get('goods_price')
        goods.goods_price_data = request.POST.get('goods_price_data')
        goods.goods_inven = request.POST.get('goods_inven')
        goods.goods_area = request.POST.get('goods_area')
        goods.goods_expr = request.POST.get('goods_expr')
        goods.goods_type = GoodsType.objects.get(type_label=request.POST.get('goods_type'))
        goods.goods_user = user
        goods.goods_photo = request.FILES.get('goods_photo')
        goods.goods_status = 1
        goods.save()
    return render(request, 'seller/goods_add.html', locals())


def change_status(request, st, id):  # 更改商品的状态
    id = int(id)
    goods = Goods.objects.filter(id=id).first()
    if st == 'up':
        goods.goods_status = 1
    elif st == 'down':
        goods.goods_status = 0
    else:
        pass
    goods.save()
    url = request.META.get('HTTP_REFERER', '/goods_list/1/1/')
    return HttpResponseRedirect(url)


# 发货
def change_order_goods_status(request, oid):  # 更改订单商品的状态
    oid = int(oid)
    order = OrderInfo.objects.filter(id=oid).first()
    order.goods_status = 2
    order.save()
    url = request.META.get('HTTP_REFERER', '/order_list/1/')
    return HttpResponseRedirect(url)
# Create your views here.
