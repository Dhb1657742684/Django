from django.shortcuts import render, HttpResponseRedirect
from Seller.models import *
import hashlib


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
        if email:
            db = User.objects.filter(email=email).first()
            if db:
                if db.password == set_pwd(password):
                    response = HttpResponseRedirect('/Seller/index/')
                    response.set_cookie('email', db.email)
                    response.set_cookie('user_id', db.id)
                    request.session['email'] = db.email
                    return response
                else:
                    err_msg = '密码错误'
            else:
                err_msg = '该邮箱尚未注册'
        else:
            err_msg = '邮箱不可为空'
    return render(request, 'seller/login.html', locals())


@loginValid
def index(request):
    return render(request, 'seller/index.html')
# Create your views here.
