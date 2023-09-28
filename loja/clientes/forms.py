#pip install Flask-WTF
#pip install wtforms.validators
#pip install wtforms
#pip install email_validator
#pip install requests
#pip install validate_docbr

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from validate_docbr import CPF, CNPJ

from loja.clientes.model import Client

cpf = CPF()
cnpj = CNPJ()


def lenght_code(form, field):
    if len(field.data) == 11:
        if cpf.validate(field.data) == False:
            raise validators.ValidationError('CPF inválido !')
    elif len(field.data) == 14:
        if cnpj.validate(field.data) == False:
            raise validators.ValidationError('CNPJ inválido !')
    else:
        raise validators.ValidationError('CPF/CNPJ inválido !')

def validacep(form, field):
    if len(field.data) == 8:
        import requests
        requests = requests.get('https://viacep.com.br/ws/{}/json/'.format(field.data))
        address_data = requests.json()
        if 'erro' in address_data:
            raise validators.ValidationError('CEP inválido !')

def validacontact(form, field):
    if (field.data.isdigit()) == False:
        raise validators.ValidationError('Contato deve somente conter números !')

class FormConta(FlaskForm):
    code = StringField('CPF/CNPJ', validators=[
                                               validators.DataRequired(message='Faltou digitar o cpf'),
                                               lenght_code])

    name = StringField('Nome', validators=[validators.Length(min=6, max=50, message="Nome deve ter no mínimo 6 e no máximo 50 caracteres"),
                                           validators.DataRequired(message='Faltou digitar o nome')])

    username = StringField('Usuário', validators=[validators.Length(min=6, max=10, message="Nome de usuário deve ter no mínimo 6 e no máximo 10 caracteres"),
                                                  validators.DataRequired('Faltou digitar o nome de usuário')])

    email = EmailField('E-mail', validators=[Length(min=6, max=60, message='E-mail deve ter entre 6 e 60 caracteres'),
                                             Email(message='Entre com um e-mail válido'),
                                             DataRequired(message='Faltou digitar o e-mail')])

    contact = StringField('Contato: ', validators=[Length(min=11, max=11, message='Contato deve ter 11 caracteres'),
                                                   DataRequired(message='Faltou digitar o contato'),
                                                   validacontact])

    password = PasswordField('Senha', validators=[DataRequired(message='Faltou digitar a senha'),
                                                  Length(min=6, message='Selecione uma senha forte')])

    confirm = PasswordField('Confirme sua senha', validators=[DataRequired(message='Faltou confirmar a sua senha'),
                                                              EqualTo('password',
                                                                          message='Senhas devem corresponder')])

    recaptcha = RecaptchaField()

    submit = SubmitField('Próximo')

    def validate_username(self, username):
        if Client.query.filter_by(username=username.data).first():
            raise ValidationError("Este usuário já existe no Banco de Dados!")

    def validate_email(self, email):
        if Client.query.filter_by(email=email.data).first():
            raise ValidationError("Este e-mail já existe no Banco de Dados!")

class FormCep(FlaskForm):

    zipcode = StringField('CEP', validators=[validators.Length(min=8, max=8, message="Cep deve ter 8 caracteres"),
                                             validators.DataRequired('Faltou digitar o cep'),
                                             validacep])

    address = StringField('Endereço', validators=[validators.Length(min=6, max=50, message="Endereço deve ter no mínimo 6 e no máximo 50 caracteres"),
                                                  validators.DataRequired('Faltou digitar o endereço')
                                                  ])

    number = StringField('Número', validators=[validators.Length(min=1, max=8, message="Número deve ter no mínimo 1 e no máximo 8 caracteres"),
                                               validators.DataRequired('Faltou digitar o número')])

    complement = StringField('Complemento')

    neighborhood = StringField('Bairro', validators=[validators.Length(min=6, max=45, message="Bairro deve ter no mínimo 6 e no máximo 45 caracteres"),
                                                     validators.DataRequired('Faltou digitar o bairro')])

    city = StringField('Cidade', validators=[validators.Length(min=6, max=45, message="Cidade deve ter no mínimo 6 e no máximo 45 caracteres"),
                                             validators.DataRequired('Faltou digitar a cidade')
                                             ])

    region = StringField('UF', validators=[validators.Length(min=2, max=2, message="UF deve ter 2 caracteres"),
                                           validators.DataRequired('Faltou digitar a Unidade da Federação')
                                           ])

    submit = SubmitField('Cadastrar')

class ClienteLoginForm(FlaskForm):
    email = StringField('E-mail: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired()])






