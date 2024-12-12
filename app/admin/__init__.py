# admin\__init__.py

from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

from . import routes  # 导入 admin 蓝图的路由 从当前模块所在包
