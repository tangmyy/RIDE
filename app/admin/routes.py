# admin\routes.py


from flask import render_template, abort, redirect, request, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

from . import admin


# 自定义管理员权限装饰器
def admin_required(f):
    """仅允许管理员访问"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:  # is_admin 字段
            abort(403)  # 禁止访问
        return f(*args, **kwargs)
    return decorated_function

# 管理后台首页
@admin.route('/dashboard')
@login_required
@admin_required  # 仅允许管理员访问
def dashboard():
    """管理员首页，显示系统的基本信息"""
    return render_template('back.html')

# 用户管理页面
@admin.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required  # 仅允许管理员访问
def select_users():
    """管理员管理用户"""
    from app.db_utils import User  # 延迟导入，避免循环依赖
    users = User.get_all_non_admin_users()
    return render_template('select_users.html', users=users)

# 新增用户页面
@admin.route('/users/add')
@login_required
@admin_required  # 仅允许管理员访问
def add():
    return render_template('add_user.html')

# 编辑用户页面
@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """编辑用户信息"""
    from app.db_utils import User  # 延迟导入，避免循环依赖
    user = User.get_user_by_id(user_id)
    if not user:
        abort(404)  # 用户不存在

    if request.method == 'POST':
        new_username = request.form.get('username')
        User.update_user(user_id, new_username)
        flash('用户信息已成功更新！', 'info')
        return redirect(url_for('admin.select_users'))

    return render_template('update_user.html', user=user)

# 删除用户功能
@admin.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """删除用户"""
    from app.db_utils import User  # 延迟导入，避免循环依赖
    User.delete_user(user_id)
    flash('用户已成功删除！', 'info')
    return redirect(url_for('admin.select_users'))

@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """新增用户"""
    from app.db_utils import User  # 延迟导入，避免循环依赖

    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # 检查输入是否为空
        if not username or not password:
            flash('用户名和密码不能为空！', 'error')
            return redirect(url_for('admin.add_user'))

        # 添加用户到数据库
        try:
            User.create_user(username, password)
            flash(f'用户 {username} 已成功创建！', 'success')
        except Exception as e:
            flash(f'新增用户失败：{str(e)}', 'error')

        return redirect(url_for('admin.select_users'))

    return render_template('add_user.html')





