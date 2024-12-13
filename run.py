# run.py
from idlelib.run import manage_socket
from flask import Flask
from flask_cors import CORS


from app.home import home_bp
from app.manage import manage_bp
app = Flask(__name__)
CORS(app, supports_credentials=True)
# 使用工厂函数创建 Flask 应用实例

app.register_blueprint(home_bp)
app.register_blueprint(manage_bp)

if __name__ == '__main__':
    app.run(debug=True)

