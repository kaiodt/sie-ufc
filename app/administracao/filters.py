# coding: utf-8


################################################################################
## SIE - UFC
################################################################################
## Filtros da View de Listagem do Painel de Administração
################################################################################


from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual, FilterNotEqual, \
                                             FilterInList, FilterNotInList

from . import admin
from .. import db


########## Funções Auxiliares ##########

# Gera as opções dos filtros via acesso ao banco de dados
def gerar_opcoes(coluna):
    with admin.app.app_context():
        return [(opcao[0], opcao[0]) for opcao in db.session.query(coluna).all()]


# Gera série de filtros para determinado campo do modelo
def FiltroOpcoes(coluna, nome):
    return [FiltroIgual(column=coluna, name=nome),
            FiltroDiferente(column=coluna, name=nome),
            FiltroNaLista(column=coluna, name=nome),
            FiltroForaDaLista(column=coluna, name=nome)]


########## Filtros ##########

# Igual a uma das opções fornecidas
class FiltroIgual(FilterEqual):
    def __init__(self, *args, **kwargs):
        super(FiltroIgual, self).__init__(*args, **kwargs)      
        self.options = gerar_opcoes(self.column)

    def operation(self):
        return 'igual'

        
# Diferente de uma das opções fornecidas
class FiltroDiferente(FilterNotEqual):
    def __init__(self, *args, **kwargs):
        super(FiltroDiferente, self).__init__(*args, **kwargs)
        self.options = gerar_opcoes(self.column)

    def operation(self):
        return 'diferente'


# Igual a alguma opção em uma lista das opções fornecidas
class FiltroNaLista(FilterInList):
    def __init__(self, *args, **kwargs):
        super(FiltroNaLista, self).__init__(*args, **kwargs)
        self.options = gerar_opcoes(self.column)

    def operation(self):
        return 'na lista'


# Diferente de todas as opções em uma lista das opções fornecidas
class FiltroForaDaLista(FilterNotInList):
    def __init__(self, *args, **kwargs):
        super(FiltroForaDaLista, self).__init__(*args, **kwargs)
        self.options = gerar_opcoes(self.column)

    def operation(self):
        return 'fora da lista'

    