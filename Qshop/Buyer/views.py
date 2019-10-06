from django.shortcuts import render, HttpResponseRedirect
from Seller.views import set_pwd
from Seller.models import *


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


@loginValid
def index(request):
    return render(request, 'buyer/index.html', locals())

# Create your views here.
