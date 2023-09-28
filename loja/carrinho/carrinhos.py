from flask import render_template, request, redirect, session, url_for, flash
from flask_login import login_required, current_user

from loja import app
from loja.produtos.models import Product, VwProduct
from loja.produtos.rotas import marcas, categorias
import json
import requests
import xml.etree.ElementTree as ET
import urllib
from xml import dom
import datetime as dt


def M_Dicionarios(dic1, dic2):
    # indica que eu já tenho os produtos na lista
    if isinstance(dic1, list) and isinstance(dic2, list):
        return dic1 + dic2
    elif isinstance(dic1, dict) and isinstance(dic2, dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False




@app.route('/addCart', methods=['POST'])
def addCart():
    try:

        produto_id = request.form.get('produto_id')
        quantity = int(request.form.get('quantity'))
        sizes = request.form.get('sizes')
        produto = VwProduct.query.filter_by(id=produto_id).first()

        if produto_id and quantity and sizes and request.method == "POST":

            desconto = float("%.2f" % (float(produto.discount / 100)))
            desconto = float("%.2f" % (desconto * float(produto.price)))
            subtotal = float("%.2f" % (float(produto.price) * int(quantity)))

            gtotal = float("%.2f" % (subtotal - desconto))
            print(gtotal)

            # Criar dicionário
            DicItems = {produto_id:{'name':produto.name, 'price':produto.price, 'discount':produto.discount,
                                    'size':sizes, 'quantity':quantity, 'image':produto.image_1, 'sizes':produto.nmsize,
                                    'freight':0, 'total':gtotal, 'subtotal':subtotal, 'format':produto.format,
                                    'weight':produto.weight, 'length':produto.length, 'height':produto.height,
                                    'width':produto.width, 'desconto':desconto, 'prazoentrega':0, 'dtentrega':""}}

            if 'LojainCarrinho' in session:
                if produto_id in session['LojainCarrinho']:
                    for key, item in session['LojainCarrinho'].items():
                        if int(key) == int(produto_id):
                            session.modified = True
                            item['quantity'] += 1

                else:
                    session['LojainCarrinho'] = M_Dicionarios(session['LojainCarrinho'], DicItems)
                    return redirect(request.referrer)
            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carros')
def getCart():

    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    valorpagar = 0
    valorfrete = 0
    numitens = 0

    for key, produto in session['LojainCarrinho'].items():

        total = float("%.2f" % produto['total'])
        frete = float("%.2f" % produto['freight'])
        valorpagar = float("%.2f" % (valorpagar + total))
        valorfrete = float("%.2f" % (valorfrete + frete))
        numitens += 1
    return render_template('produtos/carros.html', valorpagar=valorpagar, numitens=numitens,
                           subtotal=subtotal, marcas=marcas(), categorias=categorias())


@app.route('/frete')
def frete():

    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    valorpagar = 0
    valorfrete = 0
    prazoentrega = 0
    numitems = 0

    for key, produto in session['LojainCarrinho'].items():

        total = float("%.2f" % produto['total'])
        frete = float("%.2f" % produto['freight'])
        preventr = int(produto['prazoentrega'])

        valorpagar = float("%.2f" % (valorpagar + total))
        valorfrete = float("%.2f" % (valorfrete + frete))
        prazoentrega = int(prazoentrega + preventr)
        numitems = numitems + 1

    dthoje = dt.date.today()
    prazoentrega = int(prazoentrega / numitems)
    diasentrega = dt.timedelta(prazoentrega)
    dtentrega = dthoje + diasentrega

    # Colocar no forma DD/MM/YYYY
    dthoje = dthoje.strftime("%d/%m/%Y")
    dtentrega = dtentrega.strftime("%d/%m/%Y")

    return render_template('produtos/carfre.html', valorfrete=valorfrete, valorpagar=valorpagar,
                           prazoentrega=prazoentrega, subtotal=subtotal,
                           dtentrega=dtentrega, dthoje=dthoje,
                           marcas=marcas(), categorias=categorias())
@app.route('/calcular_frete')
@login_required
def calcular_frete():
    if current_user.is_authenticated:
        if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <= 0:
            return redirect(url_for('home'))
        frete = 0
        store = session['Store']
        freight_rate = (store['Taxa frete'])
        if freight_rate != 0:
            tx_frete = freight_rate / 100
        else:
            tx_frete = 0
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():

                peso = item["weight"]
                comprimento = item["length"]
                altura = item["height"]
                largura = item["width"]
                cep_destino = current_user.zipcode
                cep_origem = store["Cep origem"]
                formato = item["format"]
                codigo = "40010"

                # Busca o frete no site do correio
                freight = buscafrete(peso, comprimento, altura, largura, cep_destino, cep_origem, codigo, formato)
                if tx_frete == 0:
                    vl_frete = freight['Valor']
                    vl_frete = float(vl_frete.replace(',', '.'))
                else:
                    valorcdesc = float(item['subtotal']) - float(item['desconto'])
                    vl_frete = float(("%.2f" % (tx_frete * valorcdesc)))

                gtotal = item['total'] + vl_frete

                item['freight'] = vl_frete
                item['total'] = gtotal
                item['prazoentrega'] = freight['PrazoEntrega']

                diasentrega = int(freight['PrazoEntrega'])
                dthoje = dt.date.today()
                diasentrega = dt.timedelta(diasentrega)
                dtentrega = dthoje + diasentrega
                dtentrega = dtentrega.strftime("%d/%m/%Y")

                # Colocar no forma DD/MM/YYYY
                item['dtentrega'] = dtentrega

                print(f'Prazo de entrega do correio: {freight["PrazoEntrega"]}')
                frete += vl_frete

            return redirect(url_for('frete'))

        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
    else:
        print('current_user não autenticado')

@app.route('/updateCarro/<int:code>', methods=['POST'])
def updateCarro(code):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        size = request.form.get('sizes')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:

                    subtotal = float("%.2f" % (float(item['price']) * int(quantity)))
                    desconto = float("%.2f" % (float(item['discount'] / 100)))
                    desconto = float("%.2f" % (desconto * float(subtotal)))
                    gtotal = subtotal - desconto

                    item['quantity'] = quantity
                    item['size'] = size
                    item['desconto'] = desconto
                    item['subtotal'] = subtotal
                    item['total'] = gtotal
                    flash(f'Item foi atualizado com sucesso !', 'success')
                    return redirect(url_for('getCart'))

        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id><int:numitens>')
def deleteitem(id, numitens):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            print(numitens)
            print(int(key))
            print(id)
            if int(key) == id:
                if numitens > 1:
                    session['LojainCarrinho'].pop(key, None)
                    flash(f'Item foi removido com sucesso !', 'danger')
                    return redirect(url_for('getCart'))
                else:
                    session['LojainCarrinho'].pop(key, None)


    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/limparcarro')
def limparcarro():

    try:
        session.pop('LojainCarrinho', None)
        return redirect(url_for('home'))

    except Exception as e:
        print(e)


@app.route('/vazio')
def vazio_Cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

def buscafrete(weight, lenght, height, width, zipcode_destinacion, zipcode_origin, service, format):

    cep_origem = zipcode_origin
    cep_destino = zipcode_destinacion
    peso = weight
    comprimento = lenght
    altura = height
    largura = width
    servico = service
    formato = format

    ##### CÁLCULO FRETE #####
    # codifica os parametros para serem inclusos na url
    params = urllib.parse.urlencode({'nCdEmpresa': "",
                                     'sDsSenha': "",
                                     'sCepOrigem': cep_origem,
                                     'sCepDestino': cep_destino,
                                     'nVlPeso': peso,
                                     'nVlComprimento': comprimento,
                                     'nVlAltura': altura,
                                     'nVlLargura': largura,
                                     'nCdServico': servico,
                                     'StrRetorno': "xml",
                                     'nCdFormato': formato,
                                     'sCdMaoPropria': "n",
                                     'nVlValorDeclarado': 0,
                                     'sCdAvisoRecebimento': "n",
                                     'nVlDiametro': 0,
                                     'nIndicaCalculo': 3
                                     })


    # Lendo um XML de um web-service
    link = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?" + params

    header = {'Accept': 'application/xml'}
    response = requests.get(link, headers=header)
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    # Fazendo uma iteração geral por todos os elementos
    filtro = "*"
    for child in root.iter(filtro):
        if child.tag == 'Codigo':
            codigo = child.text
        elif child.tag == 'Valor':
            valor = child.text
        elif child.tag == 'PrazoEntrega':
            prazoentrega = child.text
        elif child.tag == 'Erro':
            erro = child.text

    #recupera os dados necessarios da folha xml
    values = {'Codigo':codigo, 'Valor':valor, 'PrazoEntrega':prazoentrega, 'Erro':erro}

    for key in values.keys():
        try:
            values[key] = dom.getElementsByTagName(key)[0].childNodes[0].nodeValue
        except:
            pass


    return {'Codigo': values['Codigo'], 'Valor': values['Valor'], 'PrazoEntrega': values['PrazoEntrega'],
            'Erro': values['Erro']}

def buscacep(zipcode):
    result_zipcode = requests.get('https://viacep.com.br/ws/{}/json/'.format(zipcode))
    address_data = result_zipcode.json()

    if 'erro' not in address_data:
        logradouro = format(address_data['logradouro'])
        localidade = format(address_data['localidade'])
        uf = format(address_data['uf'])

    values = {'Logradouro': logradouro, 'Localidade': localidade, 'Uf': uf}
    return {'Logradouro': values['Logradouro'],'Localidade': values['Localidade'],'Uf': values['Uf']}


