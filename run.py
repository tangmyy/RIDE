# run.py
import secrets

from flask import Flask, redirect

from app.db_utils import User
from app.extensions import bcrypt, login_manager

# 从软件包中 导入Blueprint蓝图对象
from app.auth import auth
from app.admin import admin
from app.alipay import alipay_bp


def create_app():
    app = Flask(__name__)

    # 自动生成随机密钥
    app.secret_key = secrets.token_hex(32)

    # 初始化扩展
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 注册蓝图
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(alipay_bp, url_prefix='/alipay')

    # 添加根路径重定向
    @app.route('/')
    def index():
        return redirect('/auth')

    return app


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login 加载用户回调"""
    return User.get_user_by_id(user_id)


# 使用工厂函数创建 Flask 应用实例

app.register_blueprint(home_bp)
if __name__ == '__main__':
    app.run(debug=True)
