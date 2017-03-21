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
from shapely import wkb     # para converter na view function 'equipamentos'


########## Rotas ##########


# Página Inicial
@principal.route('/')
def home():
    return render_template('principal/home.html')


# Página de Equipamentos
@principal.route('/equipamentos')
def equipamentos():
    # Pegando do banco de dados todos os elementos que serão inseridos no mapa
    blocos = Bloco.query.all()
    subestacoes_abrigadas = SubestacaoAbrigada.query.all()
    subestacoes_aereas = SubestacaoAerea.query.all()
    centros = Centro.query.all()
    campi = Campus.query.all()
    
    # Listas que conterão dicionários com o par objeto e localização (convertida para números de lat. e long. que podem ser processados pela extensão Leaflet)
    lista_blocos = []
    lista_subestacoes_abrigadas = []
    lista_subestacoes_aereas = []    
    lista_centros = []
    lista_campi = []

    # Processos iterativos que geram essas listas de dicionários
    for bloco in blocos:
        if bloco.localizacao is not None:    # se o bloco tiver uma localização registrada ele será adicionado à lista que será levada ao mapa
            point_temp = wkb.loads(bytes(bloco.localizacao.data))
            localizacao_temp = [point_temp.y, point_temp.x]
            lista_blocos.append({"objeto_bloco": bloco,
                                 "localizacao":  localizacao_temp
                })

    for subestacao_abrigada in subestacoes_abrigadas:
        if subestacao_abrigada.localizacao is not None:
            point_temp = wkb.loads(bytes(subestacao_abrigada.localizacao.data))
            localizacao_temp = [point_temp.y, point_temp.x]
            lista_subestacoes_abrigadas.append({"objeto_subestacao_abrigada":    subestacao_abrigada,
                                                "localizacao":                   localizacao_temp,
                })

    for subestacao_aerea in subestacoes_aereas:
        if subestacao_aerea.localizacao is not None:
            point_temp = wkb.loads(bytes(subestacao_aerea.localizacao.data))
            localizacao_temp = [point_temp.y, point_temp.x]
            lista_subestacoes_aereas.append({"objeto_subestacao_aerea":    subestacao_aerea,
                                             "localizacao":                localizacao_temp
                })

    for centro in centros:
        if centro.mapeamento is not None:
            map_temp = wkb.loads(bytes(centro.mapeamento.data)) # convertendo de um WKBElement para formato da biblioteca shapely
            mapeamento = []
            for area in list(map_temp):    # list(map_temp) retorna uma lista com os vários polygonos (ou áreas) do centro
                                           # formato: lista de tuples contendo dois elementos cada (latitude e longitude) 
                                           # Ex: [(1, 0),(1, 1),(0, 1)]
                # trocar (x,y) => (y,x)
                coordenadas_temp = []
                for ponto in list(area.exterior.coords):
                    coordenadas_temp.append([ponto[1], ponto[0]])
                mapeamento.append(coordenadas_temp)    # mapeamento é uma lista de áreas
            lista_centros.append({"objeto_centro":          centro,
                                  "mapeamento":             mapeamento,
                                  "lista_departamentos":    centro.departamentos.all()
                })

    for campus in campi:
        if campus.mapeamento is not None:
            map_temp = wkb.loads(bytes(campus.mapeamento.data))
            mapeamento = []
            for area in list(map_temp):
                coordenadas_temp = []
                for ponto in list(area.exterior.coords):
                    coordenadas_temp.append([ponto[1], ponto[0]])
                mapeamento.append(coordenadas_temp)
            lista_campi.append({"objeto_campus":        campus,
                                "mapeamento":           mapeamento
                })


    return render_template('principal/equipamentos.html', 
                            lista_blocos = lista_blocos,
                            lista_subestacoes_abrigadas = lista_subestacoes_abrigadas,
                            lista_subestacoes_aereas = lista_subestacoes_aereas,
                            lista_centros = lista_centros,
                            lista_campi = lista_campi)


# Página de Equipamentos de um Bloco
@principal.route('/equipamentos/bloco')
def equipamentos_bloco():
    id_bloco = request.args.get('id')
    bloco = Bloco.query.get(id_bloco)
    ambientes = bloco.ambientes
    local_equipamentos = []

    for ambiente in ambientes:
        local_equipamentos.extend(ambiente.equipamentos)

    dict_local_equipamentos = {}    # dicionário com a key como o tipo do equipamento e seu valor a lista de equipamentos

    for equipamento in local_equipamentos:
        if equipamento.em_uso:  # considerando apenas equipamentos em uso
            if equipamento.tipo_equipamento in dict_local_equipamentos:    # se o tipo de equipamento já possui uma key no dicionário
                dict_local_equipamentos[equipamento.tipo_equipamento].append(equipamento) # o equipamento é adicionado à lista referente à key
            else:
                dict_local_equipamentos[equipamento.tipo_equipamento] = [equipamento] # se não crio uma lista começando com o equipamento em questão

    ordem_alfa_dict = sorted(dict_local_equipamentos.iteritems())   # lista de tuples no formato (key, lista_equipamentos)
                                                                    # com keys em ordem alfabética
    return render_template('principal/equipamentos_bloco.html', 
                        bloco = bloco, ordem_alfa_dict = ordem_alfa_dict)


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
        page, per_page=10, error_out=False)

    # Lista de equipamentos após paginação

    equip_filtrados = pagination.items

    return render_template('principal/manutencoes_agendadas.html',
                           equip_man_agendada=equip_filtrados,
                           data_hoje=date.today(),
                           pagination=pagination)

