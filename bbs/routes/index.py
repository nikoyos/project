from flask import render_template, request, redirect, session, url_for, Blueprint, make_response, send_from_directory
from models.user import User
from werkzeug.utils import secure_filename
import os
from utils import log
from . import allowed_file

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


@main.route('/upload', methods=['POST'])
def upload_avatar():
    u = current_user()
    file = request.files['avatar']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 确保文件名具有安全的后缀
        if '.' not in filename:
            filename += '.jpg'
        # 保存上传的文件到服务器
        save_path = os.path.join(os.getcwd(), 'image', filename)
        file.save(save_path)
        u.user_image = filename
        u.save()
    return redirect(url_for(".profile"))




