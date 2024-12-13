import secrets

from flask import Flask, redirect
from flask_session import Session  # 确保启用 Session

from .db_utils import User
from .extensions import bcrypt, login_manager
from .auth import auth
from .admin import admin
from .alipay import alipay_bp
from .manage import manage_bp
from .home import home_bp


def create_app():
    app = Flask(__name__)

    # 配置密钥
    app.secret_key = secrets.token_hex(32)
    app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统存储会话
    app.config['SESSION_PERMANENT'] = False

    # 初始化 Session
    Session(app)

    # 初始化扩展
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 注册蓝图
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(alipay_bp, url_prefix='/alipay')
    app.register_blueprint(manage_bp, url_prefix='/manage')
    app.register_blueprint(home_bp, url_prefix='/home')

    # 添加根路径重定向
    @app.route('/')
    def index():
        return redirect('/auth')

    return app


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login 加载用户回调"""
    return User.get_user_by_id(user_id)
