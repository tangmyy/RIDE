import sqlite3

from flask import render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename

from . import manage_bp
from app.cars_db import add_car, get_all_cars, get_car_by_id, delete_car, update_car, get_cars_by_query
from app.images_db import add_image, save_vehicle_image, fetch_images_by_vehicle_id, fetch_vehicle_by_id, \
    delete_images_by_car_id, delete_vehicle_image, get_first_image_by_car_id

import os

from ..users_db import get_all_users, add_user_to_db, DATABASE, delete_user, get_user_by_id, get_users_by_query

# 定义上传目录
UPLOAD_FOLDER = os.path.join('app', 'static', 'ride')
UPLOAD_FOLDER_1 = os.path.join('ride')
# 图片上传目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 配置图片上传路径
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 显示车辆管理页面
@manage_bp.route('/cars')
def view_cars():
    """显示所有车辆，并为每辆车附加第一张图片"""
    cars = get_all_cars()

    # 将 sqlite3.Row 转换为字典，并附加图片路径
    cars_with_images = []
    for car in cars:
        car_dict = dict(car)  # 将 sqlite3.Row 转换为字典
        car_dict['image_path'] = get_first_image_by_car_id(car_dict['car_id'])  # 添加图片路径
        cars_with_images.append(car_dict)

    return render_template('manage_cars.html', cars=cars_with_images)


@manage_bp.route('/cars/add', methods=['GET', 'POST'])
def add_car_route():
    """
    添加新车辆并上传图片
    """
    if request.method == 'POST':
        # 获取表单中的车辆信息
        car_name = request.form.get('car_name')
        brand_name = request.form.get('brand_name')
        type_name = request.form.get('type_name')
        price = request.form.get('price')
        is_on_shelf = request.form.get('is_on_shelf') == '1'
        is_rented = request.form.get('is_rented') == '1'
        description = request.form.get('description', '')

        # 检查必填字段
        if not all([car_name, brand_name, type_name, price]):
            return render_template(
                'add_car.html',
                error_message="请填写所有必填字段 (除图片外)。"
            )

        # 添加车辆到数据库
        car_id = add_car(car_name, brand_name, type_name, float(price), description, is_on_shelf, is_rented)

        # 处理图片上传
        images = request.files.getlist('images')
        invalid_files = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_path_1 = os.path.join(UPLOAD_FOLDER_1, filename).replace("\\", "/")  # 替换反斜杠为斜杠
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                image.save(image_path)  # 保存图片到目录

                # 添加图片信息到数据库
                add_image(car_id, image_path_1)
            else:
                invalid_files.append(image.filename)

        # 检查是否有无效图片
        if invalid_files:
            return render_template(
                'add_car.html',
                error_message=f"以下图片文件无效：{', '.join(invalid_files)}。请上传 png, jpg, jpeg 或 gif 格式。"
            )

        return render_template('add_car.html', success_message="车辆和图片成功添加！")

    return render_template('add_car.html')


@manage_bp.route('/cars/search', methods=['GET'])
def search_cars():
    """
    根据搜索关键词返回匹配的车辆信息（JSON 格式）
    """
    query = request.args.get('query', '').strip()
    cars = []

    if query:
        cars = get_cars_by_query(query)
    else:
        cars = get_all_cars()

    return jsonify({'cars': [dict(car) for car in cars]})



@manage_bp.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car_route(car_id):
    """
    删除指定车辆
    """
    car = get_car_by_id(car_id)
    if not car:
        return jsonify({'error': '车辆未找到'}), 404

    try:
        delete_car(car_id)
        return jsonify({'message': '车辆已成功删除'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@manage_bp.route('/cars/edit/<int:car_id>', methods=['PUT'])
def edit_car_route(car_id):
    """
    修改指定车辆信息
    """
    try:
        car_name = request.json.get('car_name')
        brand_name = request.json.get('brand_name')
        type_name = request.json.get('type_name')
        price = request.json.get('price')
        description = request.json.get('description', '')

        # 检查必填字段
        if not all([car_name, brand_name, type_name, price]):
            return jsonify({'error': 'All fields except "description" are required.'}), 400

        # 更新车辆信息
        update_car(car_id, car_name=car_name, brand_name=brand_name, type_name=type_name, price=float(price),
                   description=description)
        return jsonify({'message': 'Car updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


@manage_bp.route('/users', methods=['GET'])
def view_users():
    """
    显示所有用户。
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY id ASC')  # 按 ID 升序排列
        users = cursor.fetchall()
    return render_template('view_users.html', users=users)


@manage_bp.route('/users/add', methods=['GET', 'POST'])
def add_user():
    """
    增加新用户
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == '1'

        # 检查必填字段
        if not all([username, password]):
            return "用户名和密码为必填项！"

        # 添加用户到数据库
        user_id = add_user_to_db(username, password, is_admin)

        return redirect(url_for('manage.view_users'))

    return render_template('add_user.html')


@manage_bp.route('/users/search', methods=['GET', 'POST'])
def search_users():
    """
    模糊查询用户
    """
    search_query = ''
    users = []  # 初始化空的用户列表

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()

        # 检查查询条件是否为空
        if not search_query:
            return render_template('search_users.html', users=[], search_query='请输入搜索关键词！')

        # 调用 get_users_by_query 获取匹配的用户信息
        users = get_users_by_query(search_query)

    # 无论 GET 或 POST 请求，都返回结果页面
    return render_template('search_users.html', users=users, search_query=search_query)


@manage_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    """
    删除指定用户
    """
    # 检查用户是否存在
    user = get_user_by_id(user_id)
    if not user:
        return redirect(url_for('manage.search_users', error_message='用户未找到！'))

    try:
        # 删除用户
        delete_user(user_id)
        return redirect(url_for('manage.search_users', success_message='用户成功删除！'))
    except Exception as e:
        # 记录日志或返回简单错误页面
        print(f"删除用户时发生错误：{str(e)}")  # 使用日志记录错误
        return redirect(url_for('manage.search_users', error_message='删除用户时发生错误。'))


@manage_bp.route('/vehicles/<int:vehicle_id>', methods=['GET', 'POST'])
def vehicle_details(vehicle_id):
    """
    根据车辆 ID 查询车辆详情，并为其增加图片
    """
    vehicle = fetch_vehicle_by_id(vehicle_id)

    if not vehicle:
        return render_template('vehicle_details.html', vehicle=None, error_message="车辆未找到！")

    if request.method == 'POST':
        uploaded_images = request.files.getlist('new_images')  # 获取上传的图片列表
        for image in uploaded_images:
            if image:
                save_vehicle_image(vehicle_id, image)  # 保存新图片

        return redirect(url_for('manage.vehicle_details', vehicle_id=vehicle_id))

    vehicle_images = fetch_images_by_vehicle_id(vehicle_id)
    return render_template('vehicle_details.html', vehicle=vehicle, vehicle_images=vehicle_images)


@manage_bp.route('/vehicles/delete/<int:vehicle_id>', methods=['GET', 'POST'])
def delete_images_by_vehicle(vehicle_id):
    """
    删除指定车辆的所有图片
    """
    vehicle = fetch_vehicle_by_id(vehicle_id)

    if not vehicle:
        # 如果车辆不存在，渲染带错误信息的页面
        return render_template('delete_images.html', vehicle=None, error_message="车辆未找到！")

    if request.method == 'GET':
        # 如果是 GET 请求，显示确认删除的页面
        vehicle_images = fetch_images_by_vehicle_id(vehicle_id)  # 获取车辆的所有图片
        return render_template('delete_images.html', vehicle=vehicle, vehicle_images=vehicle_images)

    # 如果是 POST 请求，执行删除操作
    delete_images_by_car_id(vehicle_id)

    # 删除后刷新车辆详情页面
    return redirect(url_for('manage.vehicle_details', vehicle_id=vehicle_id))


@manage_bp.route('/images/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    """
    删除指定图片
    """
    delete_vehicle_image(image_id)  # 删除图片及其记录
    return redirect(request.referrer or url_for('manage.view_cars'))  # 返回上一页

@manage_bp.route('/manage_cars', methods=['GET'])
def manage_cars():
    return render_template('manage_cars.html')

