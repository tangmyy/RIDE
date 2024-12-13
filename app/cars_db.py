import sqlite3

DATABASE = 'users.db'


def get_all_cars():
    """获取所有车辆信息"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        return cursor.fetchall()


def add_car(car_name, brand_name, type_name, price, description, is_on_shelf=True, is_rented=False):
    """添加新车辆"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cars (car_name, brand_name, type_name, price, description, is_on_shelf, is_rented)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (car_name, brand_name, type_name, price, description, is_on_shelf, is_rented))
        conn.commit()


def update_car(car_id, **kwargs):
    """更新车辆信息"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        fields = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [car_id]
        query = f"UPDATE cars SET {fields} WHERE car_id = ?"
        cursor.execute(query, values)
        conn.commit()


def delete_car(car_id):
    """删除车辆"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE car_id = ?", (car_id,))
        conn.commit()
