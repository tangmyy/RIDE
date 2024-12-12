# db_utils.py

import sqlite3
import logging
from flask_login import UserMixin

DATABASE = 'users.db'

# 配置日志记录
logger = logging.getLogger(__name__)

class User(UserMixin):
    def __init__(self, id, username, password, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

    @staticmethod
    def get_user_by_username_and_password(username, password):
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password, is_admin FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                if result and password == result[2]:  # 明文密码比较
                    return User(id=result[0], username=result[1], password=result[2], is_admin=result[3])
        except sqlite3.Error as e:
            logger.error(f"数据库查询失败: {e}")
        return None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password, is_admin FROM users WHERE id = ?", (user_id,))
                result = cursor.fetchone()
                if result:
                    return User(id=result[0], username=result[1], password=result[2], is_admin=result[3])
        except sqlite3.Error as e:
            logger.error(f"数据库查询失败: {e}")
        return None

    @staticmethod
    def get_all_non_admin_users():
        """获取所有非管理员用户"""
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users WHERE is_admin = 0")
            results = cursor.fetchall()
            users = [{'id': row[0], 'username': row[1]} for row in results]
            return users

    @staticmethod
    def update_user(user_id, new_username):
        """更新用户信息"""
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            conn.commit()

    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

    @staticmethod
    def create_user(username, password):
        """新增普通用户"""
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, password, 0)  # 新增用户默认不是管理员
            )
            conn.commit()



class Order:
    def __init__(self, id, user_id, total_price, time):
        self.id = id
        self.user_id = user_id
        self.total_price = total_price
        self.time = time

    @staticmethod
    def create_order(user_id, total_price, time):
        """创建新订单"""
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO orders (user_id, total_price, time) VALUES (?, ?, ?)",
                    (user_id, total_price, time)
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"创建订单失败: {e}")

    @staticmethod
    def get_latest_order_by_user(user_id):
        """获取用户最新的订单"""
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, user_id, total_price, time FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                    (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    return Order(id=result[0], user_id=result[1], total_price=result[2], time=result[3])
        except sqlite3.Error as e:
            logger.error(f"获取用户最新订单失败: {e}")
        return None

    @staticmethod
    def get_all_orders():
        """获取所有订单"""
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, user_id, total_price, time FROM orders")
                results = cursor.fetchall()
                return [
                    {'id': row[0], 'user_id': row[1], 'total_price': row[2], 'time': row[3]}
                    for row in results
                ]
        except sqlite3.Error as e:
            logger.error(f"获取所有订单失败: {e}")
        return []

    @staticmethod
    def delete_order(order_id):
        """删除订单"""
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"删除订单失败: {e}")
