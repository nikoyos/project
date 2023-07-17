from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    u = current_user()
    if u.role == 1:
        bs = Board.all()
        return render_template('board/admin_index.html', boards=bs)
    else:
        return redirect(url_for('topic.index'))
    ...


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u.role == 1:
        m = Board.new(form)
        return redirect(url_for('.index'))


@main.route('/delete')
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    if u.role == 1:
        m = Board.delete(id)
        return redirect(url_for('.index'))

