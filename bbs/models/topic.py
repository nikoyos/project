import time
from models import Model
from datetime import datetime


class Topic(Model):
    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def __init__(self, form):
        self.id = None
        self.views = 0
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = form.get('user_id', '')
        self.board_id = int(form.get('board_id', -1))

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        from .user import User
        m = User.find(self.user_id)
        return m

    def get_time_diff(self):
        current_time = int(time.time())
        time_diff = current_time - self.ct

        days, remainder = divmod(time_diff, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_diff_str = ""
        if days > 0:
            time_diff_str += f"{days}天"
        if hours > 0:
            time_diff_str += f"{hours}小时"
        if minutes > 0:
            time_diff_str += f"{minutes}分钟"
        if not time_diff_str:
            time_diff_str = "刚刚"

        return time_diff_str

