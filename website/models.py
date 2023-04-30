from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000))
    photo = db.Column(db.String(1000))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    user = db.relationship('User', backref=db.backref('answers', lazy=True))



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))
    user = db.relationship('User', backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return f"<Question {self.question}>"



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"



followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    # photo = db.Column(db.String(150), default='default.png')
    # followers relationship
    followers = db.relationship('User',
                                secondary='followers',
                                primaryjoin=(followers.c.followed_id == id),
                                secondaryjoin=(followers.c.follower_id == id),
                                backref=db.backref('following', lazy='dynamic'),
                                lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            return self

    def is_following(self, user):
        return self.following.filter(followers.c.followed_id == user.id).count() > 0

    def followed_answers(self):
        followed = Answer.query.join(
            followers, (followers.c.followed_id == Answer.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Answer.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Answer.timestamp.desc())
    
    

