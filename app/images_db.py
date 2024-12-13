import sqlite3
import os
from werkzeug.utils import secure_filename

DATABASE = 'users.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_image(car_id, image_path):
    """为指定车辆添加图片"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO car_images (car_id, image_path)
            VALUES (?, ?)
        ''', (car_id, image_path))
        conn.commit()

def get_images_by_car_id(car_id):
    """根据车辆ID获取所有图片"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM car_images WHERE car_id = ?
        ''', (car_id,))
        return cursor.fetchall()


def delete_images_by_car_id(car_id):
    """根据车辆ID删除所有相关图片"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM car_images WHERE car_id = ?
        ''', (car_id,))
        conn.commit()


def delete_car_and_images(car_id):
    """删除车辆及其相关图片"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        delete_images_by_car_id(car_id)  # 删除图片
        cursor.execute('''
            DELETE FROM cars WHERE car_id = ?
        ''', (car_id,))
        conn.commit()
