import sqlite3

def test_database_connection():
    try:
        conn = sqlite3.connect('users.db')
        conn.execute("SELECT 1")
        print("数据库连接成功！")
    except sqlite3.Error as e:
        print("数据库连接失败:", e)
    finally:
        conn.close()

# 调用测试连接函数
test_database_connection()