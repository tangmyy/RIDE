import sqlite3
import os
from werkzeug.utils import secure_filename

DATABASE = 'users.db'
UPLOAD_FOLDER = 'app/static/ride'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def get_first_image_by_car_id(car_id):
    """获取指定车辆ID的第一张图片路径"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT image_path FROM car_images 
            WHERE car_id = ? 
            ORDER BY image_id ASC LIMIT 1
        ''', (car_id,))
        result = cursor.fetchone()
        return result['image_path'] if result else None



def get_images_by_car_id(car_id):
    """获取指定车辆的所有图片路径"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT image_path FROM car_images 
            WHERE car_id = ? 
            ORDER BY image_id
        ''', (car_id,))
        return [row['image_path'] for row in cursor.fetchall()]


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


import uuid  # 用于生成唯一标识符

def save_vehicle_image(vehicle_id, image_file):
    """
    为指定车辆 ID 保存新图片，并确保文件名唯一
    """
    if not allowed_file(image_file.filename):
        raise ValueError("无效的图片类型。允许的类型：png, jpg, jpeg, gif。")

    # 确保文件名安全并生成唯一文件名
    file_extension = image_file.filename.rsplit('.', 1)[1].lower()  # 提取文件扩展名
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"  # 生成唯一文件名

    # 设置相对路径（存入数据库的路径）和文件系统中的完整路径
    relative_path = f'ride/{unique_filename}'
    image_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # 确保上传目录存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # 保存图片到文件系统
    image_file.save(image_path)

    # 将图片记录插入数据库
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO car_images (car_id, image_path)
            VALUES (?, ?)
        ''', (vehicle_id, relative_path))
        conn.commit()

def fetch_vehicle_by_id(vehicle_id):
    """
    根据车辆 ID 获取车辆详细信息
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # 返回字典格式
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM cars WHERE car_id = ?
        ''', (vehicle_id,))
        return cursor.fetchone()  # 返回单条记录


def fetch_images_by_vehicle_id(vehicle_id):
    """
    根据车辆 ID 获取所有关联图片
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM car_images WHERE car_id = ?', (vehicle_id,))
        return cursor.fetchall()


def delete_images_by_car_id(car_id):
    """
    根据车辆 ID 删除所有相关图片记录和文件
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # 获取图片路径
        cursor.execute('SELECT image_path FROM car_images WHERE car_id = ?', (car_id,))
        results = cursor.fetchall()

        for result in results:
            image_path = result[0]
            # 删除文件系统中的图片
            if os.path.exists(image_path):
                os.remove(image_path)

        # 删除数据库中的记录
        cursor.execute('DELETE FROM car_images WHERE car_id = ?', (car_id,))
        conn.commit()


def delete_vehicle_image(image_id):
    """
    根据图片 ID 删除图片记录和文件
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # 获取图片路径
        cursor.execute('SELECT image_path FROM car_images WHERE image_id = ?', (image_id,))
        result = cursor.fetchone()

        if result:
            image_path = result[0]

            # 删除文件系统中的图片
            if os.path.exists(image_path):
                os.remove(image_path)

            # 删除数据库中的记录
            cursor.execute('DELETE FROM car_images WHERE image_id = ?', (image_id,))
            conn.commit()
        else:
            print(f"图片 ID {image_id} 未找到。")

import uuid  # 用于生成唯一标识符

