# alipay\__init__.py

from flask import Blueprint

alipay_bp = Blueprint('alipay', __name__, template_folder='templates')

from . import routes    # 从当前模块所在包
