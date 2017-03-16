# coding: utf-8

################################################################################
## SIE - UFC
################################################################################
## Views do Blueprint Principal
################################################################################

from datetime import date
from flask import render_template, redirect, url_for, request

from . import principal
from ..models import *


########## Rotas ##########


# Página Inicial
@principal.route('/')
def home():
    return render_template('principal/home.html')


# Página de Equipamentos
@principal.route('/equipamentos')
def equipamentos():
    return render_template('principal/equipamentos.html')


# Página de Controle de Manutenções (Aba Manutenções Abertas)
@principal.route('/manutencoes-abertas')
def manutencoes_abertas():
    # Query de equipamentos (adicionando joins de outras tabelas)
    equip_query = Equipamento.query.join(Ambiente, Bloco, Departamento, Centro, Campus)

    # Query de equipamentos em uso
    equip_em_uso_query = equip_query.filter(Equipamento.em_uso==True)

    # Query de equipamentos em uso com manutenção aberta
    equip_em_manutencao_query = equip_em_uso_query.filter(Equipamento.em_manutencao==True)

    ##### Aqui serão aplicados outros filtros #####

    equip_filtrados_query = equip_em_manutencao_query   # Sem filtros por enquanto

    # Paginação dos resultados (ordenados por data de abertura)

    page = request.args.get('page', 1, type=int)

    pagination = equip_filtrados_query.order_by(Equipamento.inicio_manutencao).paginate(
        page, per_page=10, error_out=False)

    # Lista de equipamentos após paginação

    equip_filtrados = pagination.items

    return render_template('principal/manutencoes_abertas.html',
                           equip_man_aberta=equip_filtrados,
                           data_hoje=date.today(),
                           pagination=pagination)


# Página de Controle de Manutenções (Aba Manutenções Agendadas)
@principal.route('/manutencoes-agendadas')
def manutencoes_agendadas():
    # Query de equipamentos (adicionando joins de outras tabelas)
    equip_query = Equipamento.query.join(Ambiente, Bloco, Departamento, Centro, Campus)

    # Query de equipamentos em uso
    equip_em_uso_query = equip_query.filter(Equipamento.em_uso==True)

    # Query de equipamentos em uso com manutenção agendada (fora de manutenção)
    equip_man_agendada_query = equip_em_uso_query.filter(Equipamento.em_manutencao==False)

    ##### Aqui serão aplicados outros filtros #####

    equip_filtrados_query = equip_man_agendada_query   # Sem filtros por enquanto

    # Paginação dos resultados (ordenados por data da próxima manutenção)

    page = request.args.get('page', 1, type=int)

    pagination = equip_filtrados_query.order_by(Equipamento.proxima_manutencao).paginate(
        page, per_page=5, error_out=False)

    # Lista de equipamentos após paginação

    equip_filtrados = pagination.items

    return render_template('principal/manutencoes_agendadas.html',
                           equip_man_agendada=equip_filtrados,
                           data_hoje=date.today(),
                           pagination=pagination)

