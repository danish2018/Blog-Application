
from time import timezone
import datetime
from . import db
from flask_login import UserMixin

#  ,default=datetime.datetime.now().strftime(timeformate)
timeformate = '%d-%m-%Y %H:%M:%S'
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True , autoincrement=True)
    email = db.Column(db.String(120),unique = True)
    username = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(120),unique = True)
    contact = db.Column(db.String(15),unique = True)
    data_created =db.Column(db.String(20))
    posts = db.relationship('Post',backref ='user',passive_deletes = True)
    comments = db.relationship('Comment',backref ='user',passive_deletes = True)
    likes = db.relationship('Like',backref ='user',passive_deletes = True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.String(20))
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment',backref ='post',passive_deletes = True)
    likes = db.relationship('Like',backref ='post',passive_deletes = True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.String(20))
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created =db.Column(db.String(20))
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

