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
        from app import bcrypt  # 确保 bcrypt 被正确导入
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password, is_admin FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                if result and bcrypt.check_password_hash(result[2], password):  # 验证哈希密码
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
    def get_user_by_username(username):
        """通过用户名查询用户"""
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password, is_admin FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                if result:
                    return User(id=result[0], username=result[1], password=result[2], is_admin=result[3])
        except sqlite3.Error as e:
            logger.error(f"数据库查询失败: {e}")
        return None

    @staticmethod
    def create_user(username, password):
        """创建新用户"""
        from app import bcrypt  # 确保 bcrypt 被正确导入
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # 哈希密码
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                    (username, hashed_password, 0)  # 默认非管理员
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"创建用户失败: {e}")
            raise

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
