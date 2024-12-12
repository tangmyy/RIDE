from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# 集中管理 Flask 扩展的初始化，避免循环导入问题。

# 创建扩展实例
bcrypt = Bcrypt()
login_manager = LoginManager()

# 这里的扩展只是实例化，还没有绑定到 Flask 应用。

# extensions.py 文件的作用
# 集中管理扩展实例：
# 所有扩展（如 Flask-Bcrypt、Flask-Login）都在这里初始化为全局变量，方便在项目中使用。
# 避免循环导入问题：
# 在 Flask 项目中，扩展可能需要在 __init__.py 中被初始化，而其他模块也需要使用扩展。
# 如果扩展初始化分散到多个地方，容易出现循环导入的问题。