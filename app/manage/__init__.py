from flask import Blueprint

# 创建蓝图实例，名称改为 manage
manage_bp = Blueprint('manage', __name__, template_folder='templates', static_folder='static')

from . import routes
