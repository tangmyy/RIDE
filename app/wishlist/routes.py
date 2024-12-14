from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from . import wishlist_bp
from app.wishlist_db import add_to_wishlist, remove_from_wishlist, get_wishlist_by_user


@wishlist_bp.route('/wishlist', methods=['GET'])
@login_required
def view_wishlist():
    """显示当前用户的愿望单"""
    wishlist = get_wishlist_by_user(current_user.id)

    return render_template('wishlist.html', wishlist=wishlist)



@wishlist_bp.route('/wishlist/add/<int:car_id>', methods=['POST'])
@login_required
def add_wishlist(car_id):
    """添加车辆到愿望单"""
    success, message = add_to_wishlist(current_user.id, car_id)
    if success:
        return jsonify({"status": "success", "message": "已成功添加到愿望单！"})
    else:
        return jsonify({"status": "error", "message": "你已添加过该车辆！"})


@wishlist_bp.route('/wishlist/remove/<int:car_id>', methods=['POST'])
@login_required
def remove_wishlist(car_id):
    """从愿望单中移除车辆"""
    success, message = remove_from_wishlist(current_user.id, car_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(request.referrer or url_for('wishlist.view_wishlist'))
