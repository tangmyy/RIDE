# run.py
from flask import Flask
from app.home import home_bp
app = Flask(__name__)
# 使用工厂函数创建 Flask 应用实例

app.register_blueprint(home_bp)
if __name__ == '__main__':
    app.run(debug=True)

# test