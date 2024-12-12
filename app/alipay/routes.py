# alipay\routes.py
import sqlite3
from datetime import datetime

from flask import Blueprint, redirect, flash, request, url_for
from flask_login import login_required, current_user

from app.alipay.pay import alipay_obj, ALIPAY_SETTING

from . import alipay_bp  # 导入蓝图实例


# 数据库路径
DATABASE = 'users.db'

# 通用执行函数
def execute_query(query, params=None, fetchone=False, fetchall=False, commit=False):
    params = params or ()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()

@alipay_bp.route("/paysuccess")
def paysuccess():
    return "pay success"

@alipay_bp.route("/payfailed")
def payfail():
    return "pay fail"

# 下订单sqlite3
@alipay_bp.route("/placeorder/<int:subtotal>", methods=["POST", "GET"])
@login_required
def place_order(subtotal):
    # 获取当前时间
    cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 插入订单记录到数据库
    insert_order_query = '''
        INSERT INTO orders (user_id, total_price, time)
        VALUES (?, ?, ?)
    '''
    execute_query(insert_order_query, params=(current_user.id, subtotal, cur_time), commit=True)
    # 获取刚刚插入的订单 ID
    fetch_order_query = '''
        SELECT id FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT 1
    '''
    order = execute_query(fetch_order_query, params=(current_user.id,), fetchone=True)
    order_id = order[0]
    # 调用支付宝支付
    alipay = alipay_obj()
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="202411285777" + str(order_id),
        total_amount=subtotal,
        subject="大钻戒",
        # 支付成功回调
        return_url=ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),
        # 支付失败回调
        notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL'),
    )

    # 拼接完整支付链接
    pay_url = ALIPAY_SETTING['APIPAY_GATEWAY'] + "?" + order_string

    # 返回支付链接或重定向到支付页面
    return redirect(pay_url)


@alipay_bp.route("/alipay/success_result", methods=["GET"])
def alipay_success_result():
    alipay = alipay_obj()
    data = request.args.to_dict()
    signature = data.pop("sign", None)
    success = alipay.verify(data, signature)

    if success:
        flash("Payment successful! Thank you for your order.", "success")
        return redirect(url_for("user.home"))
    else:
        flash("Payment verification failed.", "danger")
        return redirect(url_for("user.cart"))


@alipay_bp.route("/alipay/notify_result", methods=["POST"])
def alipay_notify_result():
    alipay = alipay_obj()
    data = request.form.to_dict()
    signature = data.pop("sign", None)
    success = alipay.verify(data, signature)

    if success and data["trade_status"] in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
        # 记录回调信息
        print("Payment Notification Received:", data)
        return "success"
    return "failure"