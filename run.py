# run.py
from idlelib.run import manage_socket
from flask import Flask


from app.home import home_bp
from app.manage import manage_bp
app = Flask(__name__)
# 使用工厂函数创建 Flask 应用实例

app.register_blueprint(home_bp)
app.register_blueprint(manage_bp)

if __name__ == '__main__':
    app.run(debug=True)

