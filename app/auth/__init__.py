# auth\__init__.py

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


from . import routes  # 导入 auth 蓝图的路由 从当前模块所在包
