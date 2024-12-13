# auth\routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.db_utils import User

from . import auth  # 导入蓝图实例
from ..cars_db import get_all_cars
from ..images_db import get_first_image_by_car_id


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if not username or not password:
            flash('用户名和密码不能为空！', 'error')
        else:
            user = User.get_user_by_username_and_password(username, password)
            if user:
                login_user(user)
                if user.is_admin:  # 判断是否是管理员
                    return redirect(url_for('admin.dashboard'))  # 跳转到管理员首页
                else:
                    return redirect(url_for('auth.home'))  # 跳转到普通用户主页
            else:
                flash('用户名或密码错误，请检查输入。', 'error')
    return render_template('login.html')

@auth.route('/home')
@login_required
def home():
    """用户主页"""
    return render_template('home.html', username=current_user.username)

@auth.route('/logout')
@login_required
def logout():
    """注销用户"""
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/ride')
def ride():
    """展示所有车辆信息及其第一张图片"""
    cars = get_all_cars()  # 获取所有车辆信息
    cars_with_images = []  # 存储带图片信息的车辆数据

    for car in cars:
        car_dict = dict(car)  # 将 sqlite3.Row 转换为普通字典
        car_dict['image_path'] = get_first_image_by_car_id(car_dict['car_id'])  # 添加图片路径
        cars_with_images.append(car_dict)

    return render_template('ride.html', cars=cars_with_images)

