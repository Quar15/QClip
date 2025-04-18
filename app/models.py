from flask_login import UserMixin
from datetime import datetime, UTC
from . import db, login_manager
from .utils import EnumUserRole


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).scalar()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum(EnumUserRole), nullable=False, default=EnumUserRole.USER)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))

    def __repr__(self):
        return f"User({self.id}, '{self.username}')"


class Video(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pretty_name = db.Column(db.String(50), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    views = db.Column(db.Integer, nullable=False, default=0)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    path = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", backref=db.backref("videos"))
