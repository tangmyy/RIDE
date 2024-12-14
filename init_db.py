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

        # 插入示例订单数据
        cursor.execute(
            "INSERT OR IGNORE INTO orders (id, user_id, total_price, time) VALUES (1, 1, 100.00, '2024-11-25 03:00:00')")
        conn.commit()

        # 插入普通用户
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('lwj', '2220676', 0)")
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('zhangxing', '2220677', 0)")
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('cjcj', '2220678', 0)")
        conn.commit()
        # 插入数据
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('GPR250', 'Aprilia', '仿赛', 320.00, 1, 0, '250级别纯正仿赛')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('RS660', 'Aprilia', '仿赛', 350.00, 1, 0, '赛道操控顶级性能')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('RSV4', 'Aprilia', '仿赛', 450.00, 1, 0, '无敌公升赛道级')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('S1000RR', 'BMW', '仿赛', 750.00, 1, 0, '赛道级高性能仿赛')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('F900R', 'BMW', '街车', 500.00, 1, 0, '动力强劲的街车')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('R1250GS', 'BMW', 'ADV', 800.00, 1, 0, '全球经典越野车型')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Panigale V4', 'Ducati', '仿赛', 800.00, 1, 0, '旗舰级仿赛性能标杆')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Monster 1200', 'Ducati', '街车', 650.00, 1, 0, '街道骑行的经典之作')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Multistrada V4', 'Ducati', 'ADV', 750.00, 1, 0, '多功能的长途骑行神器')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('CBR600RR', 'Honda', '仿赛', 600.00, 1, 0, '平衡性能与易操控性')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('CB500F', 'Honda', '街车', 350.00, 1, 0, '经济实用街车')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Africa Twin', 'Honda', 'ADV', 700.00, 1, 0, '长途冒险经典')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('RC 390', 'KTM', '仿赛', 300.00, 1, 0, '轻量化仿赛性能强劲')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Duke 790', 'KTM', '街车', 420.00, 1, 0, '灵活轻巧，动力强劲')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('1290 Super Adventure', 'KTM', 'ADV', 800.00, 1, 0, '顶级ADV越野')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Ninja ZX-10R', 'Kawasaki', '仿赛', 700.00, 1, 0, '高性能仿赛之选')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Z900', 'Kawasaki', '街车', 350.00, 1, 0, '街头骑行性能首选')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Versys 1000', 'Kawasaki', 'ADV', 450.00, 1, 0, '多功能冒险骑行')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('GSX-R750', 'Suzuki', '仿赛', 600.00, 1, 0, '经典仿赛，速度与操控平衡')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('SV650', 'Suzuki', '街车', 320.00, 1, 0, '经济实用型街车')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('V-Strom 1050', 'Suzuki', 'ADV', 750.00, 1, 0, '舒适的长途旅行ADV')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('YZF-R1', 'Yamaha', '仿赛', 650.00, 1, 0, '速度与操控的完美结合')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('MT-07', 'Yamaha', '街车', 300.00, 1, 0, '街头骑行灵活轻便')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('Tracer 900', 'Yamaha', 'ADV', 500.00, 1, 0, '舒适稳定，长途旅行必备')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('800NK', '春风', '街车', 320.00, 1, 0, '国内街车高性能代表')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('650MT', '春风', 'ADV', 380.00, 1, 0, '长途骑行稳定耐用')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('300SR', '春风', '仿赛', 250.00, 1, 0, '入门级轻量仿赛')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('T310', '升仕', '街车', 300.00, 1, 0, '精致设计，灵活实用')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('T380', '升仕', '仿赛', 350.00, 1, 0, '时尚动感仿赛')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('T510', '升仕', 'ADV', 450.00, 1, 0, '强劲动力，适合越野旅行')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('500R', '无极', '街车', 300.00, 1, 0, '简洁实用的城市街车')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('500RR', '无极', '仿赛', 340.00, 1, 0, '国产高性价比仿赛')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('650ADV', '无极', 'ADV', 450.00, 1, 0, '舒适可靠，长途旅行首选')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('QJ600', '钱江', '街车', 310.00, 1, 0, '国产高性价比街车')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('QJ600GS', '钱江', '仿赛', 340.00, 1, 0, '入门级仿赛')")
        cursor.execute(
            "INSERT OR IGNORE INTO cars (car_name, brand_name, type_name, price, is_on_shelf, is_rented, description) VALUES ('QJ700ADV', '钱江', 'ADV', 400.00, 1, 0, '高性能冒险ADV')")

        # 提交更改
        conn.commit()
        # 插入管理员用户
        cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES ('admin', '123', 1)")
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


# 检查表结构
check_table_structure()