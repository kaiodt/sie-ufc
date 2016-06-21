#! coding: utf-8

from flask import Flask, render_template, flash, request, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length

from flask.ext.login import LoginManager, login_required, login_user, logout_user
from flask.ext.login import UserMixin
from flask.ext.login import current_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from werkzeug import generate_password_hash, check_password_hash

import datetime

app = Flask(__name__)
admin = Admin(app, name='sie-ufc', template_mode='bootstrap3')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ybygigmtetzayp:d-nF5hqgyp4h52VuciHozv8pPF@ec2-54-225-111-9.compute-1.amazonaws.com:5432/d6sbmnjm5hu4v8'
# app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'Y2wA&&ybkra37gDqC9cLzeH3iit4OhM!cLuJrvTjYFO-Ae]KNM'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# configuracao do sistema de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)

class Usuario(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Usuario: %r>' % self.nome

class Campus(db.Model):
    __tablename__ = 'campus'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    unidades = db.relationship('Unidade', backref='campus', lazy='dynamic')
    def __repr__(self):
        return '<Campus %r>' % self.nome


class Unidade(db.Model):
    __tablename__ = 'unidades'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64))
    departamentos = db.relationship('Departamento', backref='unidade', lazy='dynamic')
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))

    def __repr__(self):
        return '<Unidade %r>' % self.nome


class Departamento(db.Model):
    __tablename__ = 'departamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64))
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'))

    def __repr__(self):
        return '<Departamento %r>' % self.nome


class UnidadeConsumidora(db.Model):
    __tablename__ = 'unidadeconsumidora'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64))

    pos_x = db.Column(db.Float)
    pos_y = db.Column(db.Float)

    medidas = db.relationship('Medida', backref='unid_cons', lazy='dynamic')
    
    def __repr__(self):
        return '<Unidade Consumidora %r>' % self.nome

class Medida(db.Model):
    __tablename__ = 'medidas'
    id = db.Column(db.Integer, primary_key=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidadeconsumidora.id'))
    data = db.Column(db.Date)
    consumo = db.Column(db.Float)
    valor = db.Column(db.Float)

    def __repr__(self):
        return '<Medida %r>' % self.data


class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    referencia = db.Column(db.String(64), unique=True)
    
    pos_x = db.Column(db.Float)
    pos_y = db.Column(db.Float)

    def __repr__(self):
        return '<Equipamento %r>' % self.nome


class Subestacao(Equipamento):
    __tablename__ = 'subestacoes'
    id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), primary_key=True)
    potencia = db.Column(db.String(10))
    tensao = db.Column(db.String(15))

    def __repr__(self):
        return '<Subestacao %r>' % self.nome

class Religador(Equipamento):
    __tablename__ = 'religadores'
    id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), primary_key=True)
    tensao = db.Column(db.String(10))

    def __repr__(self):
        return '<Religador %r>' % self.nome

class BancoDeCapacitores(Equipamento):
    __tablename__ = 'bancodecapacitores'
    id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), primary_key=True)
    potencia = db.Column(db.String(15))
    celulas = db.Column(db.Integer)
    # estado = db.Column(db.String(20))

    def __repr__(self):
        return '<Banco de Capacitor %r>' % self.nome

class Noticia(db.Model):
    __tablename__ = 'noticias'
    id = db.Column(db.Integer, primary_key=True)
    titulo= db.Column(db.String)
    texto = db.Column(db.Text)
    data = db.Column(db.Date, default=datetime.date.today())

    def __repr__(self):
        return '<Noticia %r>' % self.titulo

class Solicitacao(db.Model):
    __tablename__ = 'solicitacao'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    descricao = db.Column(db.Text)
    estado = db.Column(db.String)
    data_abertura = db.Column(db.Date, default=datetime.date.today())
    data_encerramento = db.Column(db.Date)

    def __repr__(self):
        return '<Solicitacao %r>' % self.titulo

class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return 'Acesso Negado!' 

admin.add_view(MyModelView(Usuario, db.session))
admin.add_view(MyModelView(Subestacao, db.session, category='Equipamentos'))
admin.add_view(MyModelView(Religador, db.session, category='Equipamentos'))
admin.add_view(MyModelView(BancoDeCapacitores, db.session, category='Equipamentos'))
admin.add_view(MyModelView(Campus, db.session, category='Localizacao'))
admin.add_view(MyModelView(Unidade, db.session, category='Localizacao'))
admin.add_view(MyModelView(UnidadeConsumidora, db.session, category='Consumo'))
admin.add_view(MyModelView(Medida, db.session, category='Consumo'))
admin.add_view(MyModelView(Solicitacao, db.session))
admin.add_view(MyModelView(Noticia, db.session))


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# lógica de login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    else:
        user = request.args.get('email', type=str)
        password = request.args.get('password', type=str)
        remember = request.args.get('remember', type=bool)
        user = Usuario.query.filter_by(email=user).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/')
def index():
    noticias = Noticia.query.all()
    return render_template('index.html', noticias=noticias)

@app.route('/noticias/<id>')
def noticia(id):
    noticia = Noticia.query.filter_by(id=id)[0]
    return render_template('noticias.html', noticia=noticia)


@app.route('/equipamentos')
def equipamentos():
    subs = Subestacao.query.all()
    rels = Religador.query.all()
    caps = BancoDeCapacitores.query.all()
    return render_template('equipamentos.html',
                           subs=subs,
                           rels=rels,
                           caps=caps)

@app.route('/solicitacoes')
def solicitacoes():
    sol = Solicitacao.query.all()
    return render_template('solicitacoes.html', solicitacoes=sol)

@app.route('/consumo')
def consumo():
    unidades_consumidoras = UnidadeConsumidora.query.all()
    return render_template('consumo.html', unidades=unidades_consumidoras)

@app.route('/consumo/<id>')
def consumo_dados(id):
    unidade = UnidadeConsumidora.query.filter_by(id=id).first()
    medidas = unidade.medidas
    return render_template('consumo-dados.html', medidas=medidas, unidade=unidade)

@app.route('/graph')
def graph():
    u = UnidadeConsumidora.query.first()
    medidas = u.medidas
    return render_template('teste-grafico.html', medidas=medidas)

if __name__=='__main__':
    manager.run()