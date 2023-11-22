from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from sqlalchemy.ext import associationproxy, hybrid
from sqlalchemy.orm import validates
from datetime import datetime
import re
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
    users = db.relationship('User', back_populates='role', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Role {self.title}>'

    def __str__(self):
        return self.title


class User(UserMixin, UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'user'

    name = db.Column(db.String(config.DEFAULT_STRING_VALUE))
    email = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    phone = db.Column(db.String(config.PHONE_LENGTH), nullable=True)
    password = db.Column(db.String(config.PASSWORD_LENGTH), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', back_populates='users')

    orders = db.relationship('OrderDetail', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def __str__(self):
        return f'{self.email}: {self.name}'

    @validates('phone')
    def validate_phone(self, key, value):
        if value is not None:
            phone_pattern = re.compile(r'^\+[0-9]{11}$')
            if not phone_pattern.match(value):
                raise ValueError('Invalid phone number format. Please use a valid format.')
        return value


class AttributeCategory(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'attribute_category'

    category = db.relationship('Category', back_populates='attribute_association', primaryjoin='AttributeCategory.category_id == Category.id')
    attribute = db.relationship('Attribute', back_populates='category_association', primaryjoin='AttributeCategory.attribute_id == Attribute.id')

    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'), nullable=False)
    attribute_id = db.Column(UUID(as_uuid=True), db.ForeignKey('attribute.id'), nullable=False)


class Category(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'category'

    master_category = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'), nullable=True)
    title = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    image = db.Column(db.String(config.DEFAULT_STRING_VALUE), unique=True)
    products = db.relationship('Product', back_populates='category', lazy=True, cascade='save-update')

    # Many-to-many with Attribute
    attribute_association = db.relationship('AttributeCategory', back_populates='category')
    attributes = associationproxy.association_proxy('attribute_association', 'attribute')

    def __repr__(self):
        return f'<Category {self.title}>'

    def __str__(self):
        return self.title


class AttributeProduct(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'attribute_product'

    str_value = db.Column(db.String, nullable=True)

    attribute = db.relationship('Attribute', back_populates='product_association', primaryjoin='AttributeProduct.attribute_id == Attribute.id')
    product = db.relationship('Product', back_populates='attribute_association', primaryjoin='AttributeProduct.product_id == Product.id')

    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    attribute_id = db.Column(UUID(as_uuid=True), db.ForeignKey('attribute.id'), nullable=False)

    @hybrid.hybrid_property
    def value(self):
        match self.attribute.data_type:
            case 'int':
                return int(self.str_value) if self.str_value else None
            case 'str':
                return self.str_value if self.str_value else None
            case 'float':
                return float(self.str_value) if self.str_value else None
            # TODO добавить булевое значение

VALUE_TYPES = ('int', 'str', 'bool', 'float')

class Attribute(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'attribute'

    title = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    data_type = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False)

    # Many-to-many with Category
    category_association = db.relationship('AttributeCategory', back_populates='attribute')
    categories = associationproxy.association_proxy('category_association', 'category')

    # Many-to-many with Product
    product_association = db.relationship('AttributeProduct', back_populates='attribute')
    products = associationproxy.association_proxy('product_association', 'product')

    def __repr__(self):
        return f'<Attribute {self.title}>'


class Discount(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'discount'

    title = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=True)
    percent = db.Column(db.Integer, nullable=False)
    products = db.relationship('Product', back_populates='discount', lazy=True, cascade='save-update')

    @validates('percent')
    def validate_percent(self, key, value):
        if value < 0:
            raise ValueError('Percent cannot be less than 0.')
        return value

    def __repr__(self):
        return f'<Discount {self.title}>'
    
    def __str__(self):
        return self.title


class Brand(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'brand'

    name = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(config.DEFAULT_STRING_VALUE), unique=True)
    products = db.relationship('Product', backref='brand', lazy=True, cascade='save-update')

    def __repr__(self):
        return f'<Brand {self.name}>'


class OrderItem(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'order_item'

    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('order_detail.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)

    order = db.relationship('OrderDetail', back_populates='product_association', primaryjoin='OrderItem.order_id == OrderDetail.id')
    product = db.relationship('Product', back_populates='order_association', primaryjoin='OrderItem.product_id == Product.id')

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value < 0:
            raise ValueError('Quantity cannot be less than 0.')
        return value


class Product(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'product'

    title = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric, nullable=False)
    stock = db.Column(db.Integer, nullable=False) # Available quantity of product in stock

    discount_id = db.Column(UUID(as_uuid=True), db.ForeignKey('discount.id', ondelete='SET NULL'), nullable=True)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey('brand.id', ondelete='SET NULL'), nullable=True)
    product_images = db.relationship('ProductImage', back_populates='product', lazy=True, cascade='all, delete-orphan')

    discount = db.relationship('Discount', back_populates='products')
    category = db.relationship('Category', back_populates='products')

    # Many-to-many with OrderDetail
    order_association = db.relationship('OrderItem', back_populates='product')
    orders = associationproxy.association_proxy('order_association', 'order')

    # Many-to-many with Attribute
    attribute_association = db.relationship('AttributeProduct', back_populates='product')
    attributes = associationproxy.association_proxy('attribute_association', 'attribute')

    def __repr__(self):
        return f'<Product {self.title}>'

    def __str__(self):
        return self.title

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError('Price cannot be less than 0.')
        return value

    @validates('stock')
    def validate_stock(self, key, value):
        if value < 0:
            raise ValueError('Stock cannot be less than 0.')
        return value


class ProductImage(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'product_image'

    image = db.Column(db.String(config.DEFAULT_STRING_VALUE), unique=True)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='product_images')


class OrderDetail(UUIDMixin, TimestampMixin, db.Model):
    __tablename__ = 'order_detail'

    total = db.Column(db.Numeric, nullable=False)
    phone = db.Column(db.String(config.PHONE_LENGTH))
    address = db.Column(db.String(config.DEFAULT_STRING_VALUE), nullable=True)
    extra = db.Column(db.Text, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    # Many-to-many with Product
    product_association = db.relationship('OrderItem', back_populates='order')
    products = associationproxy.association_proxy('product_association', 'product')

    @validates('total')
    def validate_total(self, key, value):
        if value < 0:
            raise ValueError('Total cannot be less than 0.')
        return value

    @validates('phone')
    def validate_phone(self, key, value):
        if value is not None:
            phone_pattern = re.compile(r'^\+[0-9]{11}$')
            if not phone_pattern.match(value):
                raise ValueError('Invalid phone number format. Please use a valid format.')
        return value
