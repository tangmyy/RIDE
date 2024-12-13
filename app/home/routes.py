from flask import render_template
from app.cars_db import get_all_cars
from app.home import home_bp


@home_bp.route('/ride')
def ride():
    """展示所有车辆信息"""
    cars = get_all_cars()  # 从数据库获取所有车辆信息
    return render_template('ride.html', cars=cars)
