from app import db
from sqlalchemy import Table

user_board = Table("user_board", db.metadata,
                   db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
                   db.Column('board_id', db.Integer, db.ForeignKey("board.id"))
                   )
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trello_id = db.Column(db.Unicode(120), index=True, unique=True)
    username = db.Column(db.Unicode(64), index=True, unique=True)
    fullName = db.Column(db.Unicode(64), index=True, unique=True)
    # email = db.Column(db.Unicode(120), index=True, unique=True)
    boards = db.relationship('Board', secondary=user_board, backref='owner', lazy='dynamic')


    def __repr__(self):
        return '<User %r>' % self.username


class Board(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    trello_id = db.Column(db.Unicode(127))

    def __repr__(self):
        return '<Board %r>' % self.body
