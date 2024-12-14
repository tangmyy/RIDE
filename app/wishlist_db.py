import sqlite3
from datetime import datetime

DATABASE = 'users.db'


def init_wishlist_db():
    """初始化愿望单数据库表"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                car_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, car_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(car_id) REFERENCES cars(car_id)
            )
        ''')
        conn.commit()


def add_to_wishlist(user_id, car_id):
    """将车辆添加到用户的愿望单"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO wishlist (user_id, car_id)
                VALUES (?, ?)
            ''', (user_id, car_id))
            conn.commit()
            return True, "愿望已添加！"
        except sqlite3.IntegrityError:
            return False, "该车辆已在愿望单中，无法重复添加！"


def remove_from_wishlist(user_id, car_id):
    """从用户的愿望单中移除车辆"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM wishlist
            WHERE user_id = ? AND car_id = ?
        ''', (user_id, car_id))
        conn.commit()
        return True, "车辆已从愿望单中移除。"


def get_wishlist_by_user(user_id):
    """
    获取指定用户的愿望单，包含每辆车的第一张图片路径
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 联合查询获取愿望单车辆及其第一张图片
        cursor.execute('''
            SELECT cars.car_id, cars.car_name, cars.brand_name, cars.type_name, cars.price, 
                   cars.description, car_images.image_path
            FROM wishlist
            JOIN cars ON wishlist.car_id = cars.car_id
            LEFT JOIN (
                SELECT car_id, MIN(image_id) AS min_image_id
                FROM car_images
                GROUP BY car_id
            ) AS first_images ON cars.car_id = first_images.car_id
            LEFT JOIN car_images ON first_images.min_image_id = car_images.image_id
            WHERE wishlist.user_id = ?
        ''', (user_id,))

        return cursor.fetchall()