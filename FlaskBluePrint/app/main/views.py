import os
import math
import random
import datetime
import functools
from app.models import *
# from app import csrf
from hashlib import md5
from .forms import TaskForm
from app import api
from . import main
from flask_restful import Resource
from flask import jsonify  # flask 封装后的json方法
from flask_sqlalchemy import Pagination
from flask import render_template, request, redirect, session


def set_pwd(pwd):  # 密码加密
    hl = md5(pwd.encode(encoding='utf-8'))
    new_pwd = hl.hexdigest()
    return new_pwd


# def back_page(pages, current_page):  # 返回页数
#     if pages <= 5:
#         return range(1, pages + 1)
#     if current_page <= 3:
#         return range(1, 6)
#     elif current_page + 3 >= pages:
#         return range(pages - 4, pages + 1)
#     else:
#         return range(current_page - 2, current_page + 2)


def loginValid(fun):
    @functools.wraps(fun)
    def inner(*args, **kwargs):
        id = request.cookies.get('id', 0)
        username = request.cookies.get('username')
        session_username = session.get('username')
        user = User.query.get(int(id))
        if user:
            if user.username == username and username == session_username:
                return fun(*args, **kwargs)
        return redirect('/login/')

    return inner


class Calendar:  # 日历类
    def __init__(self, year=datetime.datetime.now().year, month=datetime.datetime.now().month):
        assert int(month) <= 12
        date = datetime.datetime(year, month, 1, 0, 0)  # 当前月1日
        self.start_day = date.weekday()  # 当前月1号是周几
        self.days = list(self.back_days(year, month))  # 当月天数
        self.work = ['语文', '数学', '英语', '物理', '化学', '地理', '生物']

    def back_days(self, year, month):  # 返回当月天数
        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]
        two_month = 28
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            two_month = 29
        assert int(month) <= 12
        if month in big_month:
            return range(1, 32)
        elif month in small_month:
            return range(1, 31)
        else:
            return range(1, two_month + 1)

    def first_list(self, start_day, days):  # 日历第一行
        ca_list = [{self.days.pop(0): random.choice(self.work)} for i in range(1, 8 - start_day)]
        [ca_list.insert(0, 'empty') for j in range(7 - len(ca_list))]
        return ca_list

    def return_calendar(self):  # 返回日历的列表
        first_line = self.first_list(self.start_day, self.days)  # 日历第一行
        lines = [first_line]  # 存日历的列表
        while self.days:  # 得到每一行
            line = [{self.days.pop(0): random.choice(self.work)} for i in range(7) if self.days]
            [line.append('empty') for j in range(7 - len(line))]  # 长度不足补空
            lines.append(line)
        return lines


class Paginator:
    def __init__(self, datas, page_size):
        self.datas = datas
        self.page_size = page_size
        self.all_pages = math.ceil(self.datas.count() / self.page_size)

    def back_page(self, current_page):
        if self.all_pages <= 5:
            return range(1, self.all_pages + 1)
        if current_page <= 3:
            return range(1, 6)
        elif current_page + 3 >= self.all_pages:
            return range(self.all_pages - 4, self.all_pages + 1)
        else:
            return range(current_page - 2, current_page + 2)

    def back_data(self, current_page):
        datas = self.datas.offset((current_page - 1) * self.page_size).limit(self.page_size)
        return datas


@main.route('/')  # 路由
def base():  # 视图
    # c = Curriculum(c_id='0001', c_name='python', c_time=datetime.datetime.now())
    # c.save()
    return render_template('base.html')


@main.route('/index/')  # 路由
@loginValid
def index():  # 视图
    return render_template('index.html')


@main.route('/register/', methods=['GET', 'POST'])  # 路由
def register():  # 视图
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if username:
            if email:
                if password:
                    user = User()
                    user.username = username
                    user.email = email
                    user.password = set_pwd(password)
                    user.save()
                    return redirect('/login/')
                else:
                    err_msg = '密码不可为空'
            else:
                err_msg = '邮箱不可为空'
        else:
            err_msg = '用户名不可为空'
    return render_template('register.html', **locals())


@main.route('/login/', methods=['GET', 'POST'])  # 路由
def login():  # 视图
    err_msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if set_pwd(password) == user.password:
                response = redirect('/index/')
                response.set_cookie('email', user.email)
                response.set_cookie('id', str(user.id))
                response.set_cookie('username', user.username)
                print(user.username)
                session['username'] = user.username
                return response
            else:
                err_msg = '密码错误'
        else:
            err_msg = '该账号未注册'
    return render_template('login.html', **locals())


@main.route('/logout/')
def logout():  # 退出
    response = redirect('/login/')
    response.delete_cookie('email')
    response.delete_cookie('id')
    response.delete_cookie('username')
    session.pop('username')
    return response


@main.route('/user_info/')  # 路由
@loginValid
def user_info():  # 个人中心
    c = Calendar()
    datas = c.return_calendar()
    day = datetime.datetime.now().day
    return render_template('user_info.html', **locals())


@main.route('/leave/', methods=['get', 'post'])
# @csrf.exempt
@loginValid
def leave():
    err_msg = ''
    if request.method == 'POST':
        leave_name = request.form.get('leave_name')
        leave_type = request.form.get('leave_type')
        leave_start = request.form.get('leave_start')
        leave_end = request.form.get('leave_end')
        leave_desc = request.form.get('leave_desc')
        leave_phone = request.form.get('leave_phone')
        if leave_name and leave_type and leave_start and leave_end and leave_desc and leave_phone:
            id = int(request.cookies.get('id'))
            lea = Leave()
            lea.leave_id = id
            lea.leave_name = leave_name
            lea.leave_type = leave_type
            lea.leave_start = leave_start
            lea.leave_end = leave_end
            lea.leave_desc = leave_desc
            lea.leave_phone = leave_phone
            lea.leave_status = '0'
            lea.save()
        else:
            err_msg = '请填写全部内容'
    return render_template('leave.html', **locals())


@main.route('/leave_list/<p>/', methods=['get', 'post'])
@loginValid
def leave_list(p):
    page_size = 5
    p = int(p)
    id = int(request.cookies.get('id'))
    leaves = Leave.query.filter_by(leave_id=id)
    pagin = Paginator(leaves, page_size)
    pages = pagin.back_page(p)
    leaves = pagin.back_data(p)
    return render_template('leave_list.html', **locals())


@main.route('/cancel/')
def cancel():
    id = request.args.get('id')  # 通过args接受get请求数据
    leave = Leave.query.get(int(id))
    leave.delete()
    return jsonify({'data': '删除成功'})


@main.route('/add_task/', methods=['get', 'post'])
def add_task():
    '''
    task.errors  # 表单校验错误
    task.validate_on_submit()  # 判断是否是一个有效的post请求
    task.validate()  # 判断是否是一个有效的post请求
    task.data  # 提交的数据
    :return:
    '''
    errors = {}
    task = TaskForm()
    if request.method == 'POST':
        if task.validate_on_submit():
            formData = task.data
        else:
            errors_list = list(task.errors.keys())
            errors = task.errors
            print(errors)
    return render_template('add_task.html', **locals())


@api.resource('/Api/Leave/')
class LeaveApi(Resource):
    def __init__(self):  # 定义返回的格式
        super(LeaveApi, self).__init__()
        self.result = {
            'version': '1.0',
            'data': ''
        }

    def set_data(self, leave):  # 定义返回的数据
        result_data = {
            'leave_name': leave.leave_name,
            'leave_type': leave.leave_type,
            'leave_start': leave.leave_start,
            'leave_end': leave.leave_end,
            'leave_desc': leave.leave_desc,
            'leave_phone': leave.leave_phone,
        }
        return result_data

    def get(self):
        data = request.args  # 获取请求的数据
        id = data.get('id')
        if id:
            leave = Leave.query.get(int(id))
            result_data = self.set_data(leave)
        else:
            leaves = Leave.query.all()
            result_data = []
            for leave in leaves:
                result_data.append(self.set_data(leave))
        self.result['data'] = result_data
        return self.result

    def post(self):
        data = request.form
        leave_id = data.get("leave_id")
        leave_name = data.get("leave_name")
        leave_type = data.get("leave_type")
        leave_start = data.get("leave_start")
        leave_end = data.get("leave_end")
        leave_desc = data.get("leave_desc")
        leave_phone = data.get("leave_phone")

        leave = Leave()
        leave.leave_id = leave_id
        leave.leave_name = leave_name
        leave.leave_type = leave_type  # 假期类型
        leave.leave_start = leave_start  # 起始时间
        leave.leave_end = leave_end  # 结束时间
        leave.leave_desc = leave_desc  # 请假事由
        leave.leave_phone = leave_phone  # 联系方式
        leave.leave_status = "0"  # 假条状态
        leave.save()

        self.result["data"] = self.set_data(leave)
        return self.result

    def put(self):
        data = request.form
        id = data.get('id')
        leave = Leave.query.get(int(id))
        for key, value in data.items():
            if key != 'id':
                setattr(leave, key, value)
        leave.save()
        self.result['data'] = self.set_data(leave)
        return self.result

    def delete(self):
        data = request.form
        id = data.get('id')
        leave = Leave.query.get(int(id))
        leave.delete()
        self.result['data'] = 'ID为%s的数据，删除成功' % id
        return self.result
