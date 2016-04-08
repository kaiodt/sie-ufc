from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ybygigmtetzayp:d-nF5hqgyp4h52VuciHozv8pPF@ec2-54-225-111-9.compute-1.amazonaws.com:5432/d6sbmnjm5hu4v8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Usuario %r>' % self.nome

@app.route('/')
def index():
    return render_template('index.html', name='Allana')

if __name__=='__main__':
    manager.run()