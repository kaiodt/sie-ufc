# coding: utf-8


################################################################################
## SIE - UFC
################################################################################
## Arquivo de Inicialização do Blueprint de Autenticação
################################################################################


from flask import Blueprint


########## Criação do Blueprint ##########

autenticacao = Blueprint('autenticacao', __name__)

# Importação de views

from . import views

