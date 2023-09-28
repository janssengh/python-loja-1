from loja import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

from werkzeug.security import generate_password_hash, check_password_hash

class JsonEcodeDirect(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            # retorna o dicionário
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
           # retorna vazio
           return {}
        else:
           return json.loads(value)

@login_manager.user_loader
def user_carregar(user_id):
    return Client.query.get(user_id)

class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(14), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    profile = db.Column(db.String(50), nullable=True, default='profile.jpg')
    zipcode = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    complement = db.Column(db.String(45), nullable=True)
    neighborhood = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    region = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(45), nullable=False, default='Brasil')
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    contact = db.Column(db.String(50), nullable=False)
    administrator = db.Column(db.String(1), nullable=True, default='N')

    def __init__(self, code, name, username, email, zipcode, address, number, complement,
                 neighborhood, city, region, password, type, contact):
        self.code = code
        self.name = name
        self.username = username
        self.email = email
        self.profile = self.profile
        self.zipcode = zipcode
        self.address = address
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.region = region
        self.country = self.country
        self.password = generate_password_hash(password, method='sha256')
        self.type = type
        self.contact = contact
        self.administrator = self.administrator

    def verificarSenha(self, password):  # senha sem criptografia
        return check_password_hash(self.password, password)

class ClientOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.String(20), default='pendente', nullable=False)
    client_id = db.Column(db.Integer, unique=False, nullable=False)
    created_date = db.Column(db.DateTime(50), default=datetime.utcnow, nullable=False)
    freight = db.Column(db.Numeric(15,2), nullable=False)
    amount = db.Column(db.Numeric(15,2), nullable=False)
    delivery_days = db.Column(db.Integer, nullable=False)
    order = db.Column(JsonEcodeDirect)

    def __repr__(self):
        return '<ClientOrder %r>' % self.notafiscal

class VwClientOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.String(20), default='pendente', nullable=False)
    client_id = db.Column(db.Integer, unique=False, nullable=False)
    created_date = db.Column(db.DateTime(50), default=datetime.utcnow, nullable=False)
    created_hour = db.Column(db.DateTime(50), default=datetime.utcnow, nullable=False)
    freight = db.Column(db.Numeric(15,2), nullable=False)
    amount = db.Column(db.Numeric(15,2), nullable=False)
    delivery_days = db.Column(db.Integer, nullable=False)
    order = db.Column(JsonEcodeDirect)
    delivery_date = db.Column(db.DateTime(50), default=datetime.utcnow, nullable=False)

    def __init__(self, invoice, status, client_id, created_data, created_hour, freight,
                 amount, delivery_days, order, delivery_date):
        self.invoice = invoice
        self.status = status
        self.client_id = client_id
        self.created_date = created_data
        self.created_hour = created_hour
        self.freight = freight
        self.amount = amount
        self.delivery_days = delivery_days
        self.order = order
        self.delivery_date = delivery_date


with app.app_context():
    db.create_all()
