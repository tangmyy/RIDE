from flask import Blueprint

# 创建蓝图
home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static')

# 导入蓝图的路由
from . import routes
