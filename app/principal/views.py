# coding: utf-8


################################################################################
## SIE - UFC
################################################################################
## Views do Blueprint Principal
################################################################################


from flask import render_template

from . import principal


########## Rotas ##########

# Página Inicial
@principal.route('/')
def home():
    return render_template('principal/home.html')


# Página de Equipamentos
@principal.route('/equipamentos')
def equipamentos():
    return render_template('principal/equipamentos.html')

