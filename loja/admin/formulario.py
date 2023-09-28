from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import Form, StringField, validators, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import Length, DataRequired


class RegistrationForm(Form):
    name = StringField('Nome Completo :', [validators.Length(min=4, max=25)])
    user = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Informe a sua Senha', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Senha e Confirmação não são iguais!')
    ])
    confirm = PasswordField('Informe a sua Senha Novamente')

class LoginFormulario(Form):
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Informe a sua Senha', [validators.DataRequired()])

def validacep(form, field):
    if len(field.data) == 8:
        import requests
        requests = requests.get('https://viacep.com.br/ws/{}/json/'.format(field.data))
        address_data = requests.json()
        if 'erro' in address_data:
            raise validators.ValidationError('CEP inválido !')
        else:
            logradouro = format(address_data['logradouro'])
            localidade = format(address_data['localidade'])
            uf = format(address_data['uf'])
            complemento = format(address_data['complemento'])
            bairro = format(address_data['bairro'])
            dicCep = {'logradouro': logradouro, 'localidade': localidade, 'uf': uf,
                      'complemento': complemento, 'bairro': bairro}
            session['dicCep'] = dicCep

class ZipcodeForm(FlaskForm):
    zipcode = StringField('CEP', validators=[validators.Length(min=8, max=8, message="Cep deve ter 8 caracteres"),
                                             validators.DataRequired('Faltou digitar o cep'),
                                             validacep])

    submit = SubmitField('Próximo')

def validaphone(form, field):
    if (field.data.isdigit()) == False:
        raise validators.ValidationError('Contato deve somente conter números !')

class StoreForm(FlaskForm):
    zipcode = StringField('CEP :')

    address = StringField('Endereço', validators=[validators.Length(min=6, max=50, message="Endereço deve ter no mínimo 6 e no máximo 50 caracteres"),
                                                  validators.DataRequired('Faltou digitar o endereço')
                                                  ])

    number = IntegerField('Número', validators=[validators.DataRequired('Faltou digitar o número')
                                                ])

    complement = StringField('Complemento')

    neighborhood = StringField('Bairro', validators=[validators.Length(min=6, max=45, message="Bairro deve ter no mínimo 6 e no máximo 45 caracteres"),
                                                     validators.DataRequired('Faltou digitar o bairro')])

    city = StringField('Cidade', validators=[validators.Length(min=6, max=45, message="Cidade deve ter no mínimo 6 e no máximo 45 caracteres"),
                                             validators.DataRequired('Faltou digitar a cidade')
                                             ])

    region = StringField('UF', validators=[validators.Length(min=2, max=2, message="UF deve ter 2 caracteres"),
                                           validators.DataRequired('Faltou digitar a Unidade da Federação')
                                           ])

    name = StringField('Nome', validators=[validators.Length(min=6, max=50, message="Nome deve ter no mínimo 6 e no máximo 50 caracteres"),
                                           validators.DataRequired(message='Faltou digitar o nome da loja')])

    freight_rate = IntegerField('Taxa Base Frete',[validators.NumberRange(min=0, max=50, message="Taxa frete base deve ser entre 0 e 50"),
                                                   validators.InputRequired(message="Faltou digitar a taxa base de frete")])

    pages = IntegerField('Página do site',[validators.NumberRange(min=1, message="Qtde.de produtos por página deve ser no mínimo 1"),
                                           validators.InputRequired(message="Faltou digitar a qtde.de produtos por página")])

    logo = FileField('Logotipo', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

    phone = StringField('Telefone / Celular', validators=[Length(min=11, max=11, message='Contato deve ter 11 caracteres'),
                                                   DataRequired(message='Faltou digitar o contato'),
                                                   validaphone])

    submit = SubmitField('Cadastrar')
