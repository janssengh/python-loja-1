import json
import os
import secrets

import flask
from flask import render_template, request, redirect, url_for, flash, current_app, session, make_response, jsonify
from flask_sqlalchemy_session import flask_scoped_session

from loja import app, db, photos
from .forms import Addprodutos
from .models import Brand, Product, Category, Color, Size, VwProduct, Packaging, VwPackaging
from ..admin.models import Store, VwStore


def marcas():
    marcas = Brand.query.join(VwProduct, (Brand.id == VwProduct.brand_id)).all()
    return marcas

def categorias():
    categorias = Category.query.join(VwProduct, (Category.id == VwProduct.category_id)).all()
    return categorias

def cores():
    cores = Color.query.join(VwProduct, (Color.id == VwProduct.color_id)).all()
    return cores

def tamanhos():
    tamanhos = Size.query.join(VwProduct, (Size.id == VwProduct.size_id)).all()
    return tamanhos

def embalagens():
    embalagens = VwPackaging.query.join(VwProduct, (VwPackaging.id == VwProduct.packaging_id)).all()
    return embalagens

def loja():
    loja = VwStore.query.filter_by(id=7).first()
    #return flask.jsonify(**loja.to_dict())
    return make_response(jsonify(**loja.to_dict()))

@app.route('/')
def home():

    loja_data = loja()

    session['Store'] = None
    stores = Store.query.all()
    for store in stores:
        session['Store'] = {'Cep origem': store.zipcode, 'Taxa frete': store.freight_rate,
                            'Página': store.pages}

    if not session['Store']:
        mensagem = 'Loja não registrada !! Favor solicitar ao administrador registrar...'
        return render_template('cliente/mensagem.html', mensagem=mensagem)

    pagina = request.args.get('pagina', 1, type=int)
    pages = store.pages
    produtos = VwProduct.query.filter(VwProduct.stock > 0).order_by(VwProduct.id.desc()).paginate(page=pagina, per_page=pages)
    return render_template('produtos/index.html', produtos=produtos, marcas=marcas(), categorias=categorias(),
                           tamanhos=tamanhos(), cores=cores(), embalagens=embalagens(),
                           pages=pages, store=store)

@app.route('/search/' , methods=['GET','POST'])
def search():
    pages = (session['Store']['Página'])
    if request.method == 'POST':
        form = request.form
        search_value = form['search-string']
        search = "%{0}%".format(search_value)
        pagina = request.args.get('pagina', 1, type=int)
        produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                           VwProduct.name.like(search)).order_by(VwProduct.id.desc()).paginate(page=pagina, per_page=pages)
        return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias(),
                               tamanhos=tamanhos(), cores=cores(), pages=pages, search=search)
    else:
        return redirect('/')

@app.route('/searchpage/<searchqueries>' , methods=['GET','POST'])
def searchpage(searchqueries):
    search = searchqueries
    pagina = request.args.get('pagina', 1, type=int)
    pages = (session['Store']['Página'])
    produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                       VwProduct.name.like(search)).order_by(VwProduct.id.desc()).paginate(page=pagina, per_page=pages)
    return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias(),
                            tamanhos=tamanhos(), cores=cores(), pages=pages, search=search)

@app.route('/searchall/', methods=['GET','POST'])
def searchall():

    print('entrou no searchall')
    pages = (session['Store']['Página'])

    if request.method == 'POST':
        form = request.form

        order_value = form['order-col']
        brand_id = request.form.get('marca')
        category_id = request.form.get('categoria')
        size_id = request.form.get('tamanho')
        color_id = request.form.get('cor')

        if size_id == "size_id":
            init_size_id = int("0")
            end_size_id = int("9999")
        else:
            init_size_id = int(size_id)
            end_size_id = int(size_id)

        if brand_id == "brand_id":
            init_brand_id = int("0")
            end_brand_id = int("9999")
        else:
            init_brand_id = int(brand_id)
            end_brand_id = int(brand_id)

        if category_id == "category_id":
            init_category_id = int("0")
            end_category_id = int("9999")
        else:
            init_category_id = int(category_id)
            end_category_id = int(category_id)

        if color_id == "color_id":
            init_color_id = int("0")
            end_color_id = int("9999")
        else:
            init_color_id = int(color_id)
            end_color_id = int(color_id)

        pagina = request.args.get('pagina', 1, type=int)

        if order_value == '>valor':
            produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                              ((VwProduct.size_id >= init_size_id) &
                                               (VwProduct.size_id <= end_size_id)) &
                                              ((VwProduct.brand_id >= init_brand_id) &
                                               (VwProduct.brand_id <= end_brand_id)) &
                                              ((VwProduct.category_id >= init_category_id) &
                                               (VwProduct.category_id <= end_category_id)) &
                                              ((VwProduct.color_id >= init_color_id) &
                                               (VwProduct.color_id <= end_color_id))).order_by(
                VwProduct.price.desc()).paginate(page=pagina, per_page=pages)
        else:
            if order_value == '<valor':
                produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                                  ((VwProduct.size_id >= init_size_id) &
                                                   (VwProduct.size_id <= end_size_id)) &
                                                  ((VwProduct.brand_id >= init_brand_id) &
                                                   (VwProduct.brand_id <= end_brand_id)) &
                                                  ((VwProduct.category_id >= init_category_id) &
                                                   (VwProduct.category_id <= end_category_id)) &
                                                  ((VwProduct.color_id >= init_color_id) &
                                                   (VwProduct.color_id <= end_color_id))).order_by(
                    VwProduct.price.asc()).paginate(page=pagina, per_page=pages)
            else:
                if order_value == '+recente':
                    produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                                      ((VwProduct.size_id >= init_size_id) &
                                                       (VwProduct.size_id <= end_size_id)) &
                                                      ((VwProduct.brand_id >= init_brand_id) &
                                                       (VwProduct.brand_id <= end_brand_id)) &
                                                      ((VwProduct.category_id >= init_category_id) &
                                                       (VwProduct.category_id <= end_category_id)) &
                                                      ((VwProduct.color_id >= init_color_id) &
                                                       (VwProduct.color_id <= end_color_id))).order_by(
                    VwProduct.id.desc()).paginate(page=pagina, per_page=pages)
                else:
                    produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                                      ((VwProduct.size_id >= init_size_id) &
                                                       (VwProduct.size_id <= end_size_id)) &
                                                      ((VwProduct.brand_id >= init_brand_id) &
                                                       (VwProduct.brand_id <= end_brand_id)) &
                                                      ((VwProduct.category_id >= init_category_id) &
                                                       (VwProduct.category_id <= end_category_id)) &
                                                      ((VwProduct.color_id >= init_color_id) &
                                                       (VwProduct.color_id <= end_color_id))).order_by(
                        VwProduct.discription.asc()).paginate(page=pagina, per_page=pages)

        return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias(),
                               tamanhos=tamanhos(), cores=cores(), pages=pages, order_value=order_value,
                               brand_id=brand_id, category_id=category_id, size_id=size_id, color_id=color_id)
    else:
        return redirect('/')

@app.route('/searchallpage/<brand_id>/<category_id>/<size_id>/<color_id>/<order_value>', methods=['GET', 'POST'])
def searchallpage(brand_id, category_id, size_id, color_id, order_value):

    print('entrou no searchallpage')

    pages = (session['Store']['Página'])

    brand_id = brand_id
    category_id = category_id
    size_id = size_id
    color_id = color_id
    order_value = order_value
    print(f'marca: {brand_id}')

    if size_id == "size_id":
        init_size_id = int("0")
        end_size_id = int("9999")
    else:
        init_size_id = int(size_id)
        end_size_id = int(size_id)
    if brand_id == "brand_id":
        init_brand_id = int("0")
        end_brand_id = int("9999")
    else:
        init_brand_id = int(brand_id)
        end_brand_id = int(brand_id)
    if category_id == "category_id":
        init_category_id = int("0")
        end_category_id = int("9999")
    else:
        init_category_id = int(category_id)
        end_category_id = int(category_id)
    if color_id == "color_id":
        init_color_id = int("0")
        end_color_id = int("9999")
    else:
        init_color_id = int(color_id)
        end_color_id = int(color_id)

    pagina = request.args.get('pagina', 1, type=int)

    # Ordenado por Maior Valor
    if order_value == '>valor':
        produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                              ((VwProduct.size_id >= init_size_id) &
                                               (VwProduct.size_id <= end_size_id)) &
                                              ((VwProduct.brand_id >= init_brand_id) &
                                               (VwProduct.brand_id <= end_brand_id)) &
                                              ((VwProduct.category_id >= init_category_id) &
                                               (VwProduct.category_id <= end_category_id)) &
                                              ((VwProduct.color_id >= init_color_id) &
                                               (VwProduct.color_id <= end_color_id))).order_by(
                VwProduct.price.desc()).paginate(page=pagina, per_page=pages)
    else:
        # Ordenado por Menor Valor
        if order_value == '<valor':
                produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                                  ((VwProduct.size_id >= init_size_id) &
                                                   (VwProduct.size_id <= end_size_id)) &
                                                  ((VwProduct.brand_id >= init_brand_id) &
                                                   (VwProduct.brand_id <= end_brand_id)) &
                                                  ((VwProduct.category_id >= init_category_id) &
                                                   (VwProduct.category_id <= end_category_id)) &
                                                  ((VwProduct.color_id >= init_color_id) &
                                                   (VwProduct.color_id <= end_color_id))).order_by(
                    VwProduct.price.asc()).paginate(page=pagina, per_page=pages)
        else:
            # Ordenado pelo registro mais recente do Produto
            if order_value == '+recente':
                print('entrou no +recente')
                print('redirect')
                produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                                  ((VwProduct.size_id >= init_size_id) &
                                                   (VwProduct.size_id <= end_size_id)) &
                                                  ((VwProduct.brand_id >= init_brand_id) &
                                                   (VwProduct.brand_id <= end_brand_id)) &
                                                  ((VwProduct.category_id >= init_category_id) &
                                                   (VwProduct.category_id <= end_category_id)) &
                                                  ((VwProduct.color_id >= init_color_id) &
                                                   (VwProduct.color_id <= end_color_id))).order_by(
                    VwProduct.id.desc()).paginate(page=pagina, per_page=pages)
                #return render_template('pesquisar.html', produtos=produtos)
            else:
                # Ordenado pela Descrição do Produto
                    produtos = VwProduct.query.filter((VwProduct.stock > 0) &
                                                      ((VwProduct.size_id >= init_size_id) &
                                                       (VwProduct.size_id <= end_size_id)) &
                                                      ((VwProduct.brand_id >= init_brand_id) &
                                                       (VwProduct.brand_id <= end_brand_id)) &
                                                      ((VwProduct.category_id >= init_category_id) &
                                                       (VwProduct.category_id <= end_category_id)) &
                                                      ((VwProduct.color_id >= init_color_id) &
                                                       (VwProduct.color_id <= end_color_id))).order_by(
                        VwProduct.discription.asc()).paginate(page=pagina, per_page=pages)
    return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias(),
                               tamanhos=tamanhos(), cores=cores(), pages=pages, order_value=order_value,
                               brand_id=brand_id, category_id=category_id, size_id=size_id, color_id=color_id)


@app.route('/marca/<int:id>')
def get_marca(id):
    brand_id = id

    pagina = request.args.get('pagina', 1, type=int)
    pages = (session['Store']['Página'])

    marca = VwProduct.query.filter_by(brand_id=brand_id).order_by(VwProduct.id.desc()).paginate(page=pagina, per_page=pages)

    return render_template('produtos/index.html', marca=marca, marcas=marcas(), categorias=categorias(),
                           tamanhos=tamanhos(), cores=cores(), pages=pages, brand_id=brand_id)

@app.route('/produto/<int:id>')
def pagina_unica(id):
    produto = VwProduct.query.get_or_404(id)

    marcas = Brand.query.join(VwProduct, (Brand.id == VwProduct.brand_id)).all()
    categorias = Category.query.join(VwProduct, (Category.id == VwProduct.category_id)).all()
    tamanhos = Size.query.join(VwProduct, (Size.id == VwProduct.size_id)).all()
    cores = Color.query.join(VwProduct, (Color.id == VwProduct.color_id)).all()

    return render_template('produtos/pagina_unica.html', produto=produto, marcas=marcas, categorias=categorias,
                           tamanhos=tamanhos, cores=cores)

@app.route('/categorias/<int:id>')
def get_categoria(id):
    # campo usado para paginação pgordcateg.html
    category_id = id

    pagina = request.args.get('pagina', 1, type=int)
    pages = (session['Store']['Página'])

    get_cat_prod = VwProduct.query.filter_by(category_id=category_id).order_by(VwProduct.id.desc()).paginate(page=pagina, per_page=pages)

    return render_template('produtos/index.html', get_cat_prod=get_cat_prod, categorias=categorias(), marcas=marcas(),
                           tamanhos=tamanhos(), cores=cores(), category_id=category_id, pages=pages)

@app.route('/tamanhos/<int:id>')
def get_tamanho(id):
    pagina = request.args.get('pagina', 1, type=int)
    pages = (session['Store']['Página'])

    get_tam_prod = VwProduct.query.filter_by(size_id=id).paginate(page=pagina, per_page=pages)
    marcas = Brand.query.join(VwProduct, (Brand.id == VwProduct.brand_id)).all()
    categorias = Category.query.join(VwProduct, (Category.id == VwProduct.category_id)).all()
    tamanhos = Size.query.join(VwProduct, (Size.id == VwProduct.size_id)).all()
    cores = Color.query.join(VwProduct, (Color.id == VwProduct.color_id)).all()
    return render_template('produtos/index.html', get_tam_prod=get_tam_prod, categorias=categorias,
                           marcas=marcas, tamanhos=tamanhos, cores=cores, pages=pages)

@app.route('/cores/<int:id>')
def get_cor(id):
    pagina = request.args.get('pagina', 1, type=int)
    pages = (session['Store']['Página'])

    get_cor_prod = VwProduct.query.filter_by(size_id=id).paginate(page=pagina, per_page=pages)
    marcas = Brand.query.join(VwProduct, (Brand.id == VwProduct.brand_id)).all()
    categorias = Category.query.join(VwProduct, (Category.id == VwProduct.category_id)).all()
    tamanhos = Size.query.join(VwProduct, (Size.id == VwProduct.size_id)).all()
    cores = Color.query.join(VwProduct, (Color.id == VwProduct.color_id)).all()
    return render_template('produtos/index.html', get_cor_prod=get_cor_prod, categorias=categorias,
                           marcas=marcas, tamanhos=tamanhos, cores=cores)

@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marcas = Brand(name=getmarca)
        db.session.add(marcas)
        flash(f'A marca {getmarca} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('produtos/addmarca.html', marcas='marcas')

@app.route('/updatemarca/<int:id>' , methods=['GET','POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatemarca = Brand.query.get_or_404(id)
    marcas = request.form.get('marca')
    if request.method == 'POST':
        updatemarca.name = marcas
        flash(f'Seu Fabricante foi Atualizado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))
    return render_template('produtos/updatemarca.html', titulo='Atualizar Fabricantes', updatemarca=updatemarca)

@app.route('/deletemarca/<int:id>' , methods=['POST'])
def deletemarca(id):

    marcas = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(marcas)
        db.session.commit()
        flash(f'A Marca {marcas.name} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {marcas.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))


@app.route('/updatecat/<int:id>' , methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatecat = Category.query.get_or_404(id)
    categorias = request.form.get('categoria')
    if request.method == 'POST':
        updatecat.name = categorias
        flash(f'Sua Categoria foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('produtos/updatemarca.html', titulo='Atualizar Categoria', updatecat=updatecat)

@app.route('/deletecategoria/<int:id>' , methods=['POST'])
def deletecategoria(id):

    categorias = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(categorias)
        db.session.commit()
        flash(f'A Categoria {categorias.name} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Categoria {categorias.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))




@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        cat = Category(name=getmarca)
        db.session.add(cat)
        flash(f'A categoria {getmarca} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('produtos/addmarca.html')

@app.route('/addpack', methods=['GET','POST'])
def addpack():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        format = request.form.get('format')
        weight = request.form.get('weight')
        length = request.form.get('length')
        height = request.form.get('height')
        width = request.form.get('width')
        print()

        embalagens = Packaging(format=format, weight=weight, length=length, height=height,
                               width=width)
        db.session.add(embalagens)
        flash(f'A embalagem {format} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addpack'))
    return render_template('produtos/addpack.html', embalagens='embalagens')

@app.route('/updatepack/<int:id>' , methods=['GET','POST'])
def updatepack(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatepack = Packaging.query.get_or_404(id)
    format = request.form.get('format')
    weight = request.form.get('weight')
    length = request.form.get('length')
    height = request.form.get('height')
    width = request.form.get('width')
    if updatepack.format == 1:
        discformat = "Caixa/Pacote"
    elif updatepack.format == 2:
        discformat = "Rolo/Prisma"
    else:
        discformat = "Envelope"

    if request.method == 'POST':
        updatepack.format = format
        updatepack.weight = weight
        updatepack.length = length
        updatepack.height = height
        updatepack.width = width
        flash(f'Sua Embalagem foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('embalagens'))
    return render_template('produtos/updatepack.html', titulo='Atualizar Embalagens', updatepack=updatepack,
                           discformat=discformat)

@app.route('/deletepack/<int:id>' , methods=['POST'])
def deletepack(id):

    embalagens = Packaging.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(embalagens)
        db.session.commit()
        flash(f'A Embalagem {embalagens.format} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {embalagens.format} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    marcas = Brand.query.all()
    categorias = Category.query.all()

    cores = Color.query.all()
    tamanhos = Size.query.all()

    embalagens = VwPackaging.query.all()

    form = Addprodutos(request.form)
    if request.method == "POST":

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        discription = form.discription.data

        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        # colocar numa lista o id e name da cor e separa
        coridname = request.form.get('cor')
        coridname = (coridname.split(','))
        cor = coridname[0]
        colors = coridname[1]

        tamanho = request.form.get('tamanho')
        embalagem = request.form.get('embalagem')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

        addpro = Product(name=name, price=price, discount=discount, stock=stock, colors=colors, discription=discription,
                            brand_id=marca, category_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3,
                            size_id=tamanho, color_id=cor, packaging_id=embalagem)

        db.session.add(addpro)
        flash(f'Produto {name} foi cadastrado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))


    return render_template('produtos/addproduto.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias,
                           cores=cores, tamanhos=tamanhos, embalagens=embalagens)



@app.route('/updateproduto/<int:id>' , methods=['GET','POST'])
def updateproduto(id):
    marcas = Brand.query.all()
    categorias = Category.query.all()

    cores = Color.query.all()
    tamanhos = Size.query.all()
    embalagens = VwPackaging.query.all()

    produto = Product.query.get_or_404(id)
    ########################################
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    ########################################
    cor = request.form.get('cor')
    tamanho = request.form.get('tamanho')
    ########################################
    embalagem = request.form.get('embalagem')
    vwpacks = VwPackaging.query.filter(VwPackaging.id == produto.embalagem.id)
    for vwpack in vwpacks:
        dimension = vwpack.dimension

    form = Addprodutos(request.form)
    if request.method == "POST":

        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data
        #########################################
        produto.brand_id = marca
        produto.category_id = categoria
        #########################################
        produto.color_id = cor
        produto.size_id = tamanho
        #########################################
        produto.packaging_id = embalagem
        print(produto.packaging_id)

        produto.stock = form.stock.data
        produto.colors = produto.cor.name
        produto.discription = form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Produto foi atualizado com sucesso!', 'success')
        return redirect(url_for('admin'))

    form.name.data = produto.name
    form.price.data = produto.price
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.discription.data = produto.discription

    return render_template('produtos/updateproduto.html', titulo='Atualizar Produtos', form=form, marcas=marcas,
                           categorias=categorias, produto=produto, cores=cores, tamanhos=tamanhos,
                           embalagens=embalagens, dimension=dimension)

@app.route('/deleteproduto/<int:id>' , methods=['POST'])
def deleteproduto(id):

    produto = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            if request.files.get('image_1'):
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
        except Exception as e:
            print('Erro ')


        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('admin'))

    flash(f'Produto {produto.name} foi excluído com sucesso!', 'success')

    return redirect(url_for('admin'))

@app.route('/addcor', methods=['GET','POST'])
def addcor():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getcor = request.form.get('cor')
        cores = Color(name=getcor)
        db.session.add(cores)
        flash(f'A cor {getcor} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addcor'))
    return render_template('produtos/addcor.html', cores='cores')

@app.route('/addtamanho', methods=['GET','POST'])
def addtamanho():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getcor = request.form.get('tamanho')
        tamanhos = Size(name=getcor)
        db.session.add(tamanhos)
        flash(f'O tamanho {getcor} foi cadastrado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addtamanho'))
    return render_template('produtos/addcor.html')

@app.route('/updatecor/<int:id>' , methods=['GET','POST'])
def updatecor(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatecor = Color.query.get_or_404(id)
    cores = request.form.get('cor')
    if request.method == 'POST':
        updatecor.color = cores
        flash(f'Sua Cor foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('cores'))
    return render_template('produtos/updatecor.html', titulo='Atualizar Cores', updatecor=updatecor)

@app.route('/deletecor/<int:id>' , methods=['POST'])
def deletecor(id):

    cores = Size.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(cores)
        db.session.commit()
        flash(f'A Cor {cores.color} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Cor {cores.color} não foi excluída!', 'warning')
    return redirect(url_for('admin'))


@app.route('/updatetamanho/<int:id>' , methods=['GET','POST'])
def updatetamanho(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatetamanho = Size.query.get_or_404(id)
    tamanhos = request.form.get('tamanho')
    if request.method == 'POST':
        updatetamanho.size = tamanhos
        flash(f'Seu Tamanho foi Atualizado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('tamanhos'))
    return render_template('produtos/updatecor.html', titulo='Atualizar Tamanho', updatetamanho=updatetamanho)

@app.route('/deletetamanho/<int:id>' , methods=['POST'])
def deletetamanho(id):

    tamanhos = Size.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(tamanhos)
        db.session.commit()
        flash(f'O Tamanho {tamanhos.size} foi excluído com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'O Tamanho {tamanhos.size} não foi excluído!', 'warning')
    return redirect(url_for('admin'))