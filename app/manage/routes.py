from flask import render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename

from . import manage_bp
from app.cars_db import add_car, get_all_cars, get_car_by_id, delete_car, update_car
from app.images_db import add_image

import os


# 定义上传目录
UPLOAD_FOLDER = os.path.join('manage', 'static', 'images')
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
    """显示所有车辆"""
    cars = get_all_cars()
    return render_template('manage_cars.html', cars=cars)


@manage_bp.route('/cars/add', methods=['GET', 'POST'])
def add_car_route():
    """
    添加新车辆并上传图片
    """
    if request.method == 'POST':
        try:
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
                flash('请填写所有必填字段 (除图片外)。', 'error')
                return redirect(url_for('manage.add_car_route'))

            # 添加车辆到数据库
            car_id = add_car(car_name, brand_name, type_name, float(price), description, is_on_shelf, is_rented)

            # 处理图片上传
            images = request.files.getlist('images')
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)  # 保存图片到目录

                    # 添加图片信息到数据库
                    add_image(car_id, image_path)
                else:
                    flash('上传的图片文件无效，请上传 png, jpg, jpeg 或 gif 格式。', 'error')

            flash('车辆和图片成功添加！', 'success')
            return redirect(url_for('manage.view_cars'))
        except Exception as e:
            flash(f"发生错误：{str(e)}", 'error')
            return redirect(url_for('manage.add_car_route'))

    return render_template('add_car.html')

# 删除车辆信息
@manage_bp.route('/cars/delete/<int:car_id>', methods=['DELETE'])
def delete_car_route(car_id):
    """
    删除指定车辆
    """
    try:
        car = get_car_by_id(car_id)
        if not car:
            return jsonify({'error': 'Car not found.'}), 404

        delete_car(car_id)
        return jsonify({'message': 'Car deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


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
        update_car(car_id, car_name=car_name, brand_name=brand_name, type_name=type_name, price=float(price), description=description)
        return jsonify({'message': 'Car updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500