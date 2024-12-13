import sqlite3

DATABASE = 'users.db'


def get_first_image_by_car_id(car_id):
    """获取指定车辆的第一张图片路径"""
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
            ORDER BY image_id ASC
        ''', (car_id,))
        return [row['image_path'] for row in cursor.fetchall()]


def add_image(car_id, image_path):
    """为车辆添加图片"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO car_images (car_id, image_path) 
            VALUES (?, ?)
        ''', (car_id, image_path))
        conn.commit()


def delete_image(image_id):
    """根据图片 ID 删除图片"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM car_images WHERE image_id = ?', (image_id,))
        conn.commit()
