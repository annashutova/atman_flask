from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from datetime import datetime
import uuid
import config


class UUIDMixin:
    """Inherit to add uuid primary key column to a model."""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    """Inherit to add created_at and modified_at columns to a model."""
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, onupdate=func.timezone('UTC', func.current_timestamp()), default=datetime.utcnow)


class Role(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'role'

    title = db.Column(db.String(config.DEFAULT_STRING_VALUE), unique=True)
    users = db.relationship('User', backref='user', lazy=True, cascade='all, delete-orphan')

    # def __repr__(self):
    #     return f'<Role {self.title}>'


class User(UserMixin, UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'user'

    first_name = db.Column(db.String(config.DEFAULT_STRING_VALUE))
    last_name = db.Column(db.String(config.DEFAULT_STRING_VALUE))
    email = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    password = db.Column(db.String(config.PASSWORD_LENGTH), nullable=False)
    role = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
