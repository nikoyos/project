from flask import session

from models.user import User

ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS