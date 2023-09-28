from loja import db, app

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    user = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.user

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    complement = db.Column(db.String(45), nullable=True)
    neighborhood = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    region = db.Column(db.String(15), nullable=False)
    freight_rate = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    pages = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __init__(self, zipcode, name, address, number, complement, neighborhood,
                 city, region, freight_rate, phone, pages, logo):
        self.zipcode = zipcode
        self.name = name
        self.address = address
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.region = region
        self.freight_rate = freight_rate
        self.phone = phone
        self.pages = pages
        self.logo = logo

class VwStore(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    complement = db.Column(db.String(45), nullable=True)
    neighborhood = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    region = db.Column(db.String(15), nullable=False)
    freight_rate = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    pages = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(150), nullable=False, default='image.jpg')

    def to_dict(self):
        return {
            "id": self.id,
            "zipcode": self.zipcode,
            "name": self.name,
            "address": self.address,
            "number": self.number,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "region": self.region,
            "freight_rate": self.freight_rate,
            "phone": self.phone,
            "pages": self.pages,
            "logo": self.logo}

with app.app_context():
    db.create_all()
