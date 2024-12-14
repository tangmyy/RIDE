# auth/__init__.py
from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

# 导入路由，确保导入顺序
from . import routes
