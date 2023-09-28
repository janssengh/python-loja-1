import secrets

from flask import render_template, redirect, url_for, flash, request, session, make_response
from loja import app, db, bcrypt, login_manager
from .forms import ClienteLoginForm, FormConta, FormCep
from .model import Client, ClientOrder, VwClientOrder

from flask_login import login_required, current_user, login_user, logout_user
import pdfkit
import stripe


publishable_key = 'pk_test_51MuGtwGhyM6JqwPtVWXLJqVrAcyJfZXHUHMBX46BU895l6ypXlJ0aKk8LDuPw3TzYIYmO6901OPQc2XDcIhiYcbq00VbWXO4tP'
stripe.api_key = 'sk_test_51MuGtwGhyM6JqwPtVePPrdpZ2TJqDwI17sJ98o4sVtKDErlHnd0lNUksbd2HMdvMmMmu68cj5xOZt3eewYPrcDHS008a0778UW'

@app.route('/pagamento', methods=['POST'])
@login_required
def pagamento():
    notafiscal = request.form.get('invoice')
    amount = request.form.get('amount')

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Loja_Flask',
        amount=amount,
        currency='brl',
    )

    print(f'Id: {current_user}')
    print(f'Pedido: {notafiscal}')
    print(f'Valor: {amount}')
    cliente_pedido = ClientOrder.query.filter_by(client_id=current_user.id, invoice=notafiscal).order_by(
                    ClientOrder.id.desc()).first()
    cliente_pedido.status = 'Pago'
    db.session.commit()
    mensagem = 'Obrigado por comprar conosco....Para Acompanhar seu pedido entre no menu "Meus Pedidos"!'
    return render_template('cliente/mensagem.html', mensagem=mensagem)
    #return redirect(url_for('obrigado'))


@app.route('/obrigado')
def obrigado():
    return render_template('cliente/obrigado.html')

@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = FormConta()
    return render_template('cliente/conta.html', form=form)

@app.route('/cliente/salvar', methods=['GET','POST'])
def salvar_clientes():
    form = FormConta()
    if form.validate_on_submit():
        code = form.code.data
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if len(form.code.data) > 11:
            type = 'J'
        else:
            type = 'F'
        contact = form.contact.data

        if Client.query.filter_by(code=code).first():
            form.code.errors.clear()
            form.code.errors.append('Cliente já cadastrado!')
            return render_template('formconta.html', form=form)
        else:
            # cria dicionário
            DicConta = {'code': code, 'name': name, 'username': username, 'email': email,
                        'password': password, 'type': type, 'contact': contact}
            session['DadosConta'] = DicConta
            form = FormCep()
            return render_template('cliente/cep.html', form=form)
    print(form.errors)
    return render_template('cliente/conta.html', form=form)

@app.route('/cliente/addclient', methods=['GET', 'POST'])
def addclient():
    form = FormCep()

    if form.validate_on_submit():
        DadosConta = session['DadosConta']
        code = (DadosConta['code'])
        name = (DadosConta['name'])
        username = (DadosConta['username'])
        email = (DadosConta['email'])
        password = (DadosConta['password'])
        type = (DadosConta['type'])
        contact = (DadosConta['contact'])

        zipcode = form.zipcode.data
        address = form.address.data
        number = form.number.data
        complement = form.complement.data
        neighborhood = form.neighborhood.data
        city = form.city.data
        region = form.region.data


        if Client.query.filter_by(code=code).first():
            form.code.errors.clear()
            form.code.errors.append('Cliente já cadastrado!')
            return render_template('formcep.html', form=form)
        else:
            # salva o cadastro no banco
            cadastro = Client(code, name, username, email, zipcode, address, number, complement,
                               neighborhood, city, region, password, type, contact)
            db.session.add(cadastro)
            flash(f'{name}, obrigado por cadastrar no nosso site !', 'success')
            db.session.commit()
            return redirect(url_for('clienteLogin'))
    print(form.errors)
    return render_template('cliente/cep.html', form=form)

@app.route('/cliente/login', methods=['GET','POST'])
def clienteLogin():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = Client.query.filter_by(email=form.email.data).first()
        if user and user.verificarSenha(form.password.data):
            login_user(user)
            flash(f'Voce está logado!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Senha/E-mail incorretos ou não cadastrados!', 'danger')
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/login.html', form=form)

@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('home'))


def atualizarlojaCarro():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        #del produto['image']
        del produto['sizes']
    return atualizarlojaCarro

@app.route('/pedido_order/<valorfrete>/<valorpagar>/int:<prazoentrega>')
@login_required
def pedido_order(valorfrete, valorpagar, prazoentrega):
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        freight = float(valorfrete)
        amount = float(valorpagar)
        delivery_days = prazoentrega

        atualizarlojaCarro()

        try:
            p_order = ClientOrder(invoice=notafiscal, client_id=cliente_id, amount=amount,
                                  delivery_days=delivery_days, freight=freight, order=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash(f'Seu pedido foi adicionado com sucesso !', 'success')
            return redirect(url_for('pedidos', notafiscal=notafiscal))
        except Exception as e:
            print(f'exception {e}')
            flash(f'Não foi possível processar o seu pedido !', 'danger')
            return redirect(url_for('getCart'))
    else:
        print('current_user não autenticado')

@app.route('/pedidos/<notafiscal>')
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated:
        subTotal = 0
        cliente_id = current_user.id
        cliente = Client.query.filter_by(id=cliente_id).first()
        pedidos = VwClientOrder.query.filter_by(client_id=cliente_id, invoice=notafiscal).order_by(VwClientOrder.id.desc()).first()

        frete = pedidos.freight
        dtentrega = pedidos.delivery_date
        gTotal = pedidos.amount

    else:
        return redirect(url_for('ClienteLogin'))
    return render_template('cliente/pedido.html', notafiscal=notafiscal, frete=frete, subTotal=subTotal,
                           gTotal=gTotal, dtentrega=dtentrega, cliente=cliente, pedidos=pedidos)

@app.route('/get_pdf/<notafiscal>', methods=['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated:
        subTotal = 0
        cliente_id = current_user.id

        if request.method == "POST":

            cliente = Client.query.filter_by(id=cliente_id).first()
            pedidos = VwClientOrder.query.filter_by(client_id=cliente_id, invoice=notafiscal).order_by(
                VwClientOrder.id.desc()).first()

            frete = pedidos.freight
            dtentrega = pedidos.delivery_date
            gTotal = pedidos.amount


            rendered = render_template('cliente/pdf.html', notafiscal=notafiscal, frete=frete,
                                       subTotal=subTotal, gTotal=gTotal, cliente=cliente, pedidos=pedidos,
                                       dtentrega=dtentrega)


            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            # gerar pdf
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'attached;filename='+ notafiscal+'. pdf'
            return response
    return redirect(url_for('pedidos'))

@app.route('/cliente/meuspedidos')
@login_required
def meuspedidos():
    if current_user.is_authenticated:
        client_id = current_user.id
        cliente = Client.query.filter_by(id=client_id).first()
        pedidos = VwClientOrder.query.filter_by(client_id=client_id).order_by(VwClientOrder.id.desc())
    else:
        return redirect(url_for('ClienteLogin'))
    return render_template('cliente/meuspedidos.html', pedidos=pedidos, cliente=cliente)

@app.route('/excluepedido/<int:id>', methods=['POST'])
def excluepedido(id):
    print('entrou no excluepedido')
    print(f'id: {id}')
    pedido = ClientOrder.query.get_or_404(id)
    if request.method == 'POST':
        print('entrou no POST')
        db.session.delete(pedido)
        db.session.commit()
        flash(f'O Pedido {pedido.invoice} foi excluído com sucesso!', 'success')
        return redirect(url_for('meuspedidos'))
    flash(f'O Pedido {pedido.invoice} não foi excluído!', 'warning')
    return redirect(url_for('meuspedidos'))





