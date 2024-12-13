import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'users.db'

def get_all_users():
    """获取所有用户信息"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()

def add_user_to_db(username, password, is_admin):
    """
    添加用户到数据库，密码以明文存储（仅用于测试，生产环境请加密存储）。
    返回新增用户的 ID。
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, is_admin)
            VALUES (?, ?, ?)
        ''', (username, password, is_admin))
        conn.commit()
        return cursor.lastrowid  # 返回新插入记录的自增 ID

def get_user_by_id(user_id):
    """
    根据用户 ID 获取用户信息
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

def get_users_by_query(search_query):
    """
    模糊查询用户
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE username LIKE ?
        ''', (f'%{search_query}%',))
        return cursor.fetchall()


def delete_user(user_id):
    """
    删除用户
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
