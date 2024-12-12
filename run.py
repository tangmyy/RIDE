# run.py

from app import create_app

# 使用工厂函数创建 Flask 应用实例
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
