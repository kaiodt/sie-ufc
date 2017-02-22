# coding: utf-8


################################################################################
## SIE - UFC
################################################################################
## Formatos de Alguns Campos das Views do Painel de Administração
################################################################################


from flask import request, url_for
from datetime import date
from jinja2 import Markup
from flask_admin.contrib.geoa import typefmt
from wtforms.widgets import html_params
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement
from sqlalchemy import func


########## Formatos de Tipos de Dados ##########

# Tipo Data
def formato_data(view, value):
    return value.strftime('%d.%m.%Y')


# Tipo Mapa
def formato_mapa(view, value):
    # Alterar dimensões do mapa na view de detalhes
    if 'details' in request.path:
        width = 400
        height = 400
        zoom = 17
    else:
        width = 100
        height = 70
        zoom = 15

    params = html_params(**{
        "data-role": "leaflet",
        "data-width": width,
        "data-height": height,
        "data-geometry-type": to_shape(value).geom_type,
        "data-zoom": zoom
    })

    # Desabilitar edição na view de listar
    if 'details' not in request.path:
        params += u' disabled'

    if value.srid is -1:
        value.srid = 4326

    geojson = view.session.query(view.model).with_entities(func.ST_AsGeoJSON(value)).scalar()

    return Markup('<textarea %s>%s</textarea>' % (params, geojson))


########## Formatos de Campos Específicos ##########

# Campos Tipo Relação
def formato_relacao(view, context, model, name):
    return model.__getattribute__(name).all()


########## Registro dos Formatos de Tipos de Dados ##########

FORMATOS_PADRAO = dict(typefmt.DEFAULT_FORMATTERS)
FORMATOS_PADRAO[date] = formato_data
FORMATOS_PADRAO[WKBElement] = formato_mapa

