import os
import sqlite3

from app import bcrypt

# 定义数据库路径（确保指向 app/users.db）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'users.db')


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # 创建 users 表，列名为 is_admin
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )''')

        # 创建 order 表
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        # 创建 cars 表
        cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
               car_id INTEGER PRIMARY KEY AUTOINCREMENT,
               car_name TEXT NOT NULL,
               brand_name TEXT NOT NULL,
               type_name TEXT NOT NULL,
               price REAL NOT NULL,
               is_on_shelf BOOLEAN NOT NULL DEFAULT 1,
               is_rented BOOLEAN NOT NULL DEFAULT 0
           )''')
        # 添加 description 列到 cars 表
        cursor.execute('''
                       ALTER TABLE cars ADD COLUMN description TEXT
                       ''')

        print("描述列已添加到 cars 表中")
        # 创建 car_images 表
        cursor.execute('''
              CREATE TABLE IF NOT EXISTS car_images (
                  image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  car_id INTEGER NOT NULL,
                  image_path TEXT NOT NULL,
                  FOREIGN KEY (car_id) REFERENCES cars(car_id)
              )
              ''')

        # 创建 rental 表
        cursor.execute('''CREATE TABLE IF NOT EXISTS rental (
               rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               car_id INTEGER NOT NULL,
               rent_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
               return_date DATETIME NULL,
               FOREIGN KEY(car_id) REFERENCES cars(car_id)
           )''')

        # 插入示例订单数据
        cursor.execute(
            "INSERT OR IGNORE INTO orders (id, user_id, total_price, time) VALUES (1, 1, 100.00, '2024-11-25 03:00:00')")
        conn.commit()

        # 插入普通用户
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('lwj', '2220676', 0)")
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('zhangxing', '2220677', 0)")
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('cjcj', '2220678', 0)")
        conn.commit()

        # 插入管理员用户
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('admin', '123', 1)")
        conn.commit()
        # 插入示例数据到 cars 表
        cars_data = [
            ('Camry', 'Kawasaki', '街车', 300.00, 1, 0),
            ('Camry', 'Yamaha', '街车', 300.00, 1, 0),
            ('Model S', 'Ducati', '仿赛', 500.00, 1, 0),
            ('Civic', 'Honda', '街车', 250.00, 1, 0),
            ('Accord', 'Suzuki', '街车', 280.00, 0, 0),
            ('Accord', 'Aprilia', '仿赛', 280.00, 0, 0),
            ('X5', 'BMW', 'ADV', 400.00, 1, 0),
            ('X5', '春风', 'ADV', 400.00, 1, 0),
            ('X5', '钱江', 'ADV', 400.00, 1, 0),
            ('X5', '无极', 'ADV', 400.00, 1, 0),
            ('X5', '升仕', 'ADV', 400.00, 1, 0),
            ('X5', 'KTM', '越野', 400.00, 1, 0)
        ]
        cursor.executemany('''
           INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented)
           VALUES (?, ?, ?, ?, ?, ?)''', cars_data)
        conn.commit()

        # 插入示例数据到 rental 表
        cursor.execute('''
           INSERT OR IGNORE INTO rental (rental_id, user_id, car_id, rent_date)
           VALUES (1, 1, 1, '2024-12-01 10:00:00')''')
        conn.commit()
        print("数据库初始化完成")


# 初始化数据库
init_db()


def check_table_structure():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # 检查 users 表结构
        print("Users table structure:")
        cursor.execute("PRAGMA table_info(users)")
        users_columns = cursor.fetchall()
        for column in users_columns:
            print(column)

        # 检查 orders 表结构
        print("\nOrders table structure:")
        cursor.execute("PRAGMA table_info(orders)")
        orders_columns = cursor.fetchall()
        for column in orders_columns:
            print(column)

        print("Cars table structure:")
        cursor.execute("PRAGMA table_info(cars)")
        cars_columns = cursor.fetchall()
        for column in cars_columns:
            print(column)

        # 检查 rental 表结构
        print("\nRental table structure:")
        cursor.execute("PRAGMA table_info(rental)")
        rental_columns = cursor.fetchall()
        for column in rental_columns:
            print(column)


# 检查表结构
check_table_structure()
