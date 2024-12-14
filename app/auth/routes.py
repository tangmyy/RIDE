# auth\routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.db_utils import User

from . import auth  # 导入蓝图实例
from ..cars_db import get_all_cars, get_car_by_id, get_cars_by_query, get_unique_brands
from ..images_db import get_first_image_by_car_id, fetch_images_by_vehicle_id


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


from app.cars_db import get_all_cars, get_cars_by_query, get_unique_brands, get_unique_types


from app.cars_db import get_price_range

@auth.route('/ride', methods=['GET', 'POST'])
@login_required
def ride():
    """
    车辆信息页面，支持搜索、品牌筛选、车型筛选、价格排序和价格区间筛选功能
    """
    selected_brand = None  # 存储选择的品牌
    selected_type = None  # 存储选择的车型
    sort_order = None  # 存储价格排序选项
    min_price = None  # 最低价格筛选
    max_price = None  # 最高价格筛选

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        selected_brand = request.form.get('brand', None)
        selected_type = request.form.get('type', None)
        sort_order = request.form.get('sort_order', None)
        min_price = request.form.get('min_price', None)
        max_price = request.form.get('max_price', None)

        # 根据搜索和筛选条件获取车辆
        cars = get_cars_by_query(search_query) if search_query else get_all_cars()
        if selected_brand and selected_brand != "all":
            cars = [car for car in cars if car['brand_name'] == selected_brand]
        if selected_type and selected_type != "all":
            cars = [car for car in cars if car['type_name'] == selected_type]
        if min_price:
            cars = [car for car in cars if car['price'] >= float(min_price)]
        if max_price:
            cars = [car for car in cars if car['price'] <= float(max_price)]

        # 按价格排序
        if sort_order == "asc":
            cars.sort(key=lambda x: x['price'])
        elif sort_order == "desc":
            cars.sort(key=lambda x: x['price'], reverse=True)
    else:
        cars = get_all_cars()

    # 提取品牌、车型和价格区间
    brands = get_unique_brands()
    types = get_unique_types()
    price_range = get_price_range()

    # 将 sqlite3.Row 转换为字典，并附加图片路径
    cars_with_images = []
    for car in cars:
        car_dict = dict(car)  # 将 sqlite3.Row 转换为字典
        car_dict['image_path'] = get_first_image_by_car_id(car_dict['car_id'])  # 添加图片路径
        cars_with_images.append(car_dict)

    return render_template(
        'ride.html',
        cars=cars_with_images,
        brands=brands,
        types=types,
        price_range=price_range,
        selected_brand=selected_brand,
        selected_type=selected_type,
        sort_order=sort_order,
        min_price=min_price,
        max_price=max_price
    )



@auth.route('/car/<int:car_id>', methods=['GET'])
@login_required
def car_details(car_id):
    """
    显示指定车辆的详细信息
    """
    car = get_car_by_id(car_id)
    if not car:
        flash("车辆不存在！", "error")
        return redirect(url_for('auth.home'))

    images = fetch_images_by_vehicle_id(car_id)  # 获取该车辆的所有图片
    return render_template('car_details.html', car=car, images=images)
