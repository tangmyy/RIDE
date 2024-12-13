import sqlite3

DATABASE = 'users.db'


def add_car(car_name, brand_name, type_name, price, description, is_on_shelf=True, is_rented=False):
    """添加新车辆并返回其 ID"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cars (car_name, brand_name, type_name, price, description, is_on_shelf, is_rented)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (car_name, brand_name, type_name, price, description, is_on_shelf, is_rented))
        car_id = cursor.lastrowid
        conn.commit()
        return car_id


def get_all_cars():
    """获取所有车辆信息"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars')
        return cursor.fetchall()


def get_car_by_id(car_id):
    """根据车辆 ID 获取车辆信息"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = ?', (car_id,))
        return cursor.fetchone()


def delete_car(car_id):
    """删除指定车辆"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
        conn.commit()


def update_car(car_id, **kwargs):
    """更新车辆信息"""
    fields = ', '.join(f"{key} = ?" for key in kwargs.keys())
    values = list(kwargs.values()) + [car_id]

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE cars
            SET {fields}
            WHERE id = ?
        ''', values)
        conn.commit()
