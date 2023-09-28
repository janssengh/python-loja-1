from flask import render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Product, Brand, Category, Color, Size, Packaging
from loja import app, db, bcrypt, LoginManager
from .formulario import RegistrationForm, LoginFormulario, ZipcodeForm, StoreForm
from .models import User, Store


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    produtos = Product.query.all()
    return render_template('admin/index.html', titulo='Administrador', produtos=produtos)

@app.route('/loja')
def loja():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    loja = Store.query.all()
    return render_template('admin/loja.html', titulo='Pagina Loja', loja=loja)

@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    #marcas = Marca.query.all()
    marcas = Brand.query.order_by(Brand.id.desc()).all()

    return render_template('admin/marca.html', titulo='Pagina Fabricantes', marcas=marcas)

@app.route('/categoria')
def categoria():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    #categorias = Categoria.query.all()
    categorias = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/marca.html', titulo='Pagina Categorias', categorias=categorias)

@app.route('/cores')
def cores():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    cores = Color.query.order_by(Color.id.desc()).all()

    return render_template('admin/cor.html', titulo='Pagina Cores', cores=cores)

@app.route('/tamanhos')
def tamanhos():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    tamanhos = Size.query.order_by(Size.id.desc()).all()

    return render_template('admin/cor.html', titulo='Pagina Tamanhos', tamanhos=tamanhos)

@app.route('/embalagens')
def embalagens():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    embalagens = Packaging.query.order_by(Packaging.id.desc()).all()

    return render_template('admin/embalagem.html', titulo='Pagina Embalagens', embalagens=embalagens)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, user=form.user.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por registrar !','success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, titulo='Registrar')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginFormulario(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'{form.email.data} logado com sucesso!', 'success')
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('Não foi possível acessar o sistema!', 'danger')
    return render_template('admin/login.html', form=form, titulo='Login')

@app.route('/ceploja', methods=['GET','POST'])
def ceploja():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    loja = Store.query.all()
    if loja:
        flash(f'Loja já foi registrada!', 'danger')
        return redirect(url_for('admin'))
    form = ZipcodeForm()
    return render_template('admin/ceploja.html', form=form)

@app.route('/parametrosloja', methods=['GET','POST'])
def parametrosloja():
    form = ZipcodeForm()
    if form.validate_on_submit():
        # Dados pesquisados VIACEP no formulário do CEP
        dicCep = session['dicCep']
        localidade = (dicCep['localidade'])
        uf = (dicCep['uf'])
        bairro = (dicCep['bairro'])
        complemento = (dicCep['complemento'])
        logradouro = (dicCep['logradouro'])

        # cria dicionário
        zipcode = form.zipcode.data
        DicZipcode = {'zipcode': zipcode}
        session['ZipCode'] = DicZipcode

        form = StoreForm()
        form.city.data = localidade
        form.region.data = uf
        form.neighborhood.data = bairro
        form.complement.data = complemento
        form.address.data = logradouro

        return render_template('admin/addloja.html', form=form)
    return render_template('admin/ceploja.html', form=form)

@app.route('/addloja', methods=['GET','POST'])
def addloja():
    form = StoreForm()
    if form.validate_on_submit():
        ZipCode = session['ZipCode']
        zipcode = (ZipCode['zipcode'])
        address = form.address.data
        number = form.number.data
        complement = form.complement.data
        neighborhood = form.neighborhood.data
        city = form.city.data
        region = form.region.data
        freight_rate = form.freight_rate.data
        name = form.name.data
        pages = form.pages.data
        phone = form.phone.data
        logo = form.logo.data

        loja = Store(zipcode, name, address, number, complement, neighborhood, city,
                         region, freight_rate, phone, pages, logo)

        db.session.add(loja)
        flash(f'A loja {name} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/addloja.html', form=form)

@app.route('/updateloja/<int:id>' , methods=['GET','POST'])
def updateloja(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updateloja = Store.query.get_or_404(id)
    name = request.form.get('name')
    freight = request.form.get('freight')
    pages = request.form.get('pages')

    if request.method == 'POST':
        updateloja.name = name
        updateloja.freight_rate = freight
        updateloja.pages = pages
        flash(f'Sua Loja foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('loja'))
    return render_template('admin/updateloja.html', titulo='Atualizar Fabricantes', updateloja=updateloja)

@app.route('/deleteloja/<int:id>' , methods=['POST'])
def deleteloja(id):

    loja = Store.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(loja)
        db.session.commit()
        flash(f'A Loja {loja.name} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Loja {loja.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))
