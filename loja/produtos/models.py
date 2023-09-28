from loja import db, app

from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    discription = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    marca = db.relationship('Brand', backref=db.backref('marcas', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    categoria = db.relationship('Category', backref=db.backref('categorias', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    cor = db.relationship('Color', backref=db.backref('cores', lazy=True))

    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    nmsize = db.relationship('Size', backref=db.backref('sizes', lazy=True))
    tamanho = db.relationship('Size', backref=db.backref('tamanhos', lazy=True))
    packaging_id = db.Column(db.Integer, db.ForeignKey('packaging.id'), nullable=False)
    embalagem = db.relationship('Packaging', backref=db.backref('embalagens', lazy=True))

    def __repr__(self):
        return '<Product %r>' % self.name

class VwProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    discription = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, nullable=False)
    nmbrand = db.Column(db.String(30), nullable=False)

    category_id = db.Column(db.Integer,  nullable=False)
    nmcategory = db.Column(db.String(30), nullable=False)

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    color_id = db.Column(db.Integer, nullable=False)
    nmcolor = db.Column(db.String(20), nullable=False)

    size_id = db.Column(db.Integer, nullable=False)
    nmsize = db.Column(db.String(20), nullable=False)

    packaging_id = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.String(4), nullable=False)
    format = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Numeric(15, 2), nullable=False)
    height = db.Column(db.Numeric(15, 2), nullable=False)
    width = db.Column(db.Numeric(15, 2), nullable=False)

    def __repr__(self):
        return '<VwProduct %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

class Packaging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.String(20), nullable=False)
    format = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Numeric(15, 2), nullable=False)
    height = db.Column(db.Numeric(15, 2), nullable=False)
    width = db.Column(db.Numeric(15, 2), nullable=False)

class VwPackaging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dimension = db.Column(db.String(45), nullable=False)


with app.app_context():
    db.create_all()
