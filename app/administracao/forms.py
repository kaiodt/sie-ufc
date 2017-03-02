# coding: utf-8

################################################################################
## SIE - UFC
################################################################################
## Fomulários do Painel de Administração
################################################################################


from datetime import date
from flask import request
from flask_wtf import FlaskForm
from flask_admin.form.fields import Select2Field, Select2TagsField
from flask_admin.form.widgets import DatePickerWidget
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.contrib.geoa.fields import GeoJSONField
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DecimalField, \
                    SubmitField, TextAreaField, DateField
from wtforms import ValidationError
from wtforms.validators import InputRequired, Email, Length, Regexp, NumberRange, EqualTo

from .. import db
from ..models import *
from .fields import DateFieldMod


########## Formulário Base (Com Tradução) ##########


class FormBase(FlaskForm):
    class Meta:
        locales = ['pt_BR']


########## Formulários para os Modelos do Sistema ##########


# Edição de Cargo
class FormEditarCargo(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 36),
                               Regexp(u'[A-Za-z ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    permissoes = IntegerField('Permissões', validators=[InputRequired(),
                                                        NumberRange(0, 255)])

    padrao = BooleanField('Padrão')

    usuarios = QuerySelectMultipleField('Usuários',
                                        query_factory=lambda: Usuario.query.all(),
                                        allow_blank=True)


# Criação de Usuário
class FormCriarUsuario(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    email = StringField('Email', validators=[InputRequired(),
                                             Length(1, 64),
                                             Email()])

    senha = PasswordField('Senha', validators=[InputRequired(),
                                               Length(6, 16)])

    cargo = QuerySelectField('Cargo', query_factory=lambda: Cargo.query.all())

    confirmado = BooleanField('Confirmado')


    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('Email já cadastrado.')


# Edição de Usuário
class FormEditarUsuario(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    email = StringField('Email', validators=[InputRequired(),
                                             Length(1, 64),
                                             Email()])

    cargo = QuerySelectField('Cargo', query_factory=lambda: Cargo.query.all())

    confirmado = BooleanField('Confirmado')


    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first() and \
                field.data != Usuario.query.get(request.args.get('id')).email:
            raise ValidationError('Email já cadastrado.')


# Criação de Instituição
class FormCriarInstituicao(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])


# Edição de Instituição
class FormEditarInstituicao(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    campi = QuerySelectMultipleField('Campi', query_factory=lambda: Campus.query.all(),
                                              allow_blank=True)


# Criação de Campus
class FormCriarCampus(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    instituicao = QuerySelectField('Instituição',
                                   query_factory=lambda: Instituicao.query.all())

    mapeamento = GeoJSONField('Mapeamento', srid=-1, session=db.session,
                              geometry_type= 'MULTIPOLYGON',
                              render_kw={'data-width':400, 'data-height':400,
                                         'data-zoom':10,
                                         'data-lat':-3.7911773, 'data-lng':-38.5893123})


# Edição de Campus
class FormEditarCampus(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    instituicao = QuerySelectField('Instituição',
                                   query_factory=lambda: Instituicao.query.all())

    mapeamento = GeoJSONField('Mapeamento', srid=-1, session=db.session,
                              geometry_type= 'MULTIPOLYGON',
                              render_kw={'data-width':400, 'data-height':400})

    centros = QuerySelectMultipleField('Centros', query_factory=lambda: Centro.query.all(),
                                                  allow_blank=True)


# Criação de Centro
class FormCriarCentro(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    campus = QuerySelectField('Campus', query_factory=lambda: Campus.query.all())

    mapeamento = GeoJSONField('Mapeamento', srid=-1, session=db.session,
                              geometry_type= 'MULTIPOLYGON',
                              render_kw={'data-width':400, 'data-height':400,
                                         'data-zoom':10,
                                         'data-lat':-3.7911773, 'data-lng':-38.5893123})


# Edição de Centro
class FormEditarCentro(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    campus = QuerySelectField('Campus', query_factory=lambda: Campus.query.all())

    mapeamento = GeoJSONField('Mapeamento', srid=-1, session=db.session,
                              geometry_type= 'MULTIPOLYGON',
                              render_kw={'data-width':400, 'data-height':400})

    departamentos = QuerySelectMultipleField('Departamentos', 
                                             query_factory=lambda: Departamento.query.all(),
                                             allow_blank=True)


# Criação de Departamento
class FormCriarDepartamento(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    centro = QuerySelectField('Centro', query_factory=lambda: Centro.query.all())


# Edição de Departamento
class FormEditarDepartamento(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    centro = QuerySelectField('Centro', query_factory=lambda: Centro.query.all())

    blocos = QuerySelectMultipleField('Blocos', query_factory=lambda: Bloco.query.all(),
                                                allow_blank=True)


# Criação de Bloco
class FormCriarBloco(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    departamento = QuerySelectField('Departamento',
                                    query_factory=lambda: Departamento.query.all())

    localizacao = GeoJSONField('Localização', srid=-1, session=db.session,
                                geometry_type= 'POINT',
                                render_kw={'data-width':400, 'data-height':400,
                                           'data-zoom':10,
                                           'data-lat':-3.7911773, 'data-lng':-38.5893123})


# Edição de Bloco
class FormEditarBloco(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    departamento = QuerySelectField('Departamento',
                                    query_factory=lambda: Departamento.query.all())

    localizacao = GeoJSONField('Localização', srid=-1, session=db.session,
                               geometry_type= 'POINT',
                               render_kw={'data-width':400, 'data-height':400})

    ambientes = QuerySelectMultipleField('Ambientes',
                                         query_factory=lambda: Ambiente.query.all(),
                                         allow_blank=True)


# Criação de Ambiente
class FormCriarAmbiente(FormBase):
    tipo_ambiente = Select2Field('', choices=[('ambienteinterno', 'Ambiente Interno'),
                                              ('ambienteexterno', 'Ambiente Externo'),
                                              ('subestacaoabrigada', 'Subestação Abrigada'),
                                              ('subestacaoaerea', 'Subestação Aérea')],
                                     validators=[InputRequired()])

    proximo = SubmitField('Próximo')


# Criação de Ambiente Interno
class FormCriarAmbienteInterno(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    andar = Select2Field('Andar',
      choices=[('Térreo', 'Térreo')] + [(str(n)+'º Andar', str(n)+'º Andar') 
               for n in range(1, 11)])

    bloco = QuerySelectField('Bloco', query_factory=lambda: Bloco.query.all())

    detalhe_localizacao = TextAreaField('Detalhe de Localização')

    area = DecimalField('Área (m²)', places=2, validators=[NumberRange(0)])

    populacao = IntegerField('População', validators=[NumberRange(0)])


# Edição de Ambiente Interno
class FormEditarAmbienteInterno(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    andar = Select2Field('Andar',
      choices=[('Térreo', 'Térreo')] + [(str(n)+'º Andar', str(n)+'º Andar')
               for n in range(1, 11)])    

    bloco = QuerySelectField('Bloco', query_factory=lambda: Bloco.query.all())

    detalhe_localizacao = TextAreaField('Detalhe de Localização')

    area = DecimalField('Área (m²)', places=2, validators=[NumberRange(0)])

    populacao = IntegerField('População', validators=[NumberRange(0)])

    equipamentos = QuerySelectMultipleField('Equipamentos',
                                            query_factory=lambda: Equipamento.query.all(),
                                            allow_blank=True)


# Criação de Ambiente Externo
class FormCriarAmbienteExterno(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    bloco = QuerySelectField('Bloco', query_factory=lambda: Bloco.query.all())

    detalhe_localizacao = TextAreaField('Detalhe de Localização')


# Edição de Ambiente Externo
class FormEditarAmbienteExterno(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    bloco = QuerySelectField('Bloco', query_factory=lambda: Bloco.query.all())

    detalhe_localizacao = TextAreaField('Detalhe de Localização')

    equipamentos = QuerySelectMultipleField('Equipamentos',
                                            query_factory=lambda: Equipamento.query.all(),
                                            allow_blank=True)


# Criação de Subestação Abrigada
class FormCriarSubestacaoAbrigada(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    bloco = QuerySelectField('Bloco', 
        query_factory=lambda: Bloco.query.filter(Bloco.nome.like('Subestações%')).all())

    localizacao = GeoJSONField('Localização', srid=-1, session=db.session,
                               geometry_type= 'POINT',
                               render_kw={'data-width':400, 'data-height':400,
                                          'data-zoom':10,
                                          'data-lat':-3.7911773, 'data-lng':-38.5893123})

    detalhe_localizacao = TextAreaField('Detalhe de Localização')


# Edição de Subestação Abrigada
class FormEditarSubestacaoAbrigada(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    bloco = QuerySelectField('Bloco', 
        query_factory=lambda: Bloco.query.filter(Bloco.nome.like('Subestações%')).all())

    localizacao = GeoJSONField('Localização', srid=-1, session=db.session,
                               geometry_type= 'POINT',
                               render_kw={'data-width':400, 'data-height':400})

    detalhe_localizacao = TextAreaField('Detalhe de Localização')

    equipamentos = QuerySelectMultipleField('Equipamentos', 
                                            query_factory=lambda: Equipamento.query.all(),
                                            allow_blank=True)


# Criação de Subestação Aérea
class FormCriarSubestacaoAerea(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    bloco = QuerySelectField('Bloco', 
        query_factory=lambda: Bloco.query.filter(Bloco.nome.like('Subestações%')).all())

    localizacao = GeoJSONField('Localização', srid=-1, session=db.session,
                               geometry_type= 'POINT',
                               render_kw={'data-width':400, 'data-height':400,
                                          'data-zoom':10,
                                          'data-lat':-3.7911773, 'data-lng':-38.5893123})

    detalhe_localizacao = TextAreaField('Detalhe de Localização')


# Edição de Subestação Aérea
class FormEditarSubestacaoAerea(FormBase):
    nome = StringField('Nome', validators=[InputRequired(),
                               Length(1, 64),
                               Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    bloco = QuerySelectField('Bloco', 
        query_factory=lambda: Bloco.query.filter(Bloco.nome.like('Subestações%')).all())

    localizacao = GeoJSONField('Localização', srid=-1, session=db.session,
                               geometry_type= 'POINT',
                               render_kw={'data-width':400, 'data-height':400})

    detalhe_localizacao = TextAreaField('Detalhe de Localização')

    equipamentos = QuerySelectMultipleField('Equipamentos',
                                            query_factory=lambda: Equipamento.query.all(),
                                            allow_blank=True)


# Criação de Equipamento
class FormCriarEquipamento(FormBase):
    tipo_equipamento = Select2Field('', choices=[('extintor', 'Extintor')],
                                        validators=[InputRequired()])

    proximo = SubmitField('Próximo')


# Criação de Extintor
class FormCriarExtintor(FormBase):
    tombamento = IntegerField('Tombamento', validators=[NumberRange(0)])

    classificacao = Select2Field('Classificação', 
                                 choices=[('Água [A]', 'Água [A]'),
                                          ('Espuma [AB]', 'Espuma [AB]'),
                                          ('CO2 [BC]', 'CO2 [BC]'),
                                          ('Pó Químico [BC]', 'Pó Químico [BC]'),
                                          ('Pó Químico [ABC]', 'Pó Químico [ABC]')],
                                 validators=[InputRequired()])

    carga_nominal = DecimalField('Carga Nominal (kg)', places=2, 
                                                       validators=[NumberRange(0)])

    fabricante = StringField('Fabricante',
                             validators=[Length(1, 64),
                             Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    ambiente = QuerySelectField('Ambiente', query_factory=lambda: Ambiente.query.all())

    intervalo_manutencao = IntegerField('Intervalo de Manutenção (Meses)',
                                        validators=[InputRequired(), NumberRange(0)])
                                                                               
    em_uso = BooleanField('Em Uso')

    info_adicional = TextAreaField('Informações Adicionais')                         


    def validate_tombamento(self, field):
        if field.data != 0:
            if Equipamento.query.filter_by(tombamento=field.data).first():
                raise ValidationError('Equipamento já cadastrado.')


# Edição de Extintor
class FormEditarExtintor(FormBase):
    tombamento = IntegerField('Tombamento', validators=[NumberRange(0)])

    classificacao = Select2Field('Classificação', 
                                 choices=[('Água [A]', 'Água [A]'),
                                          ('Espuma [AB]', 'Espuma [AB]'),
                                          ('CO2 [BC]', 'CO2 [BC]'),
                                          ('Pó Químico [BC]', 'Pó Químico [BC]'),
                                          ('Pó Químico [ABC]', 'Pó Químico [ABC]')],
                                 validators=[InputRequired()])

    carga_nominal = DecimalField('Carga Nominal (kg)', places=2,
                                                       validators=[NumberRange(0)])

    fabricante = StringField('Fabricante',
                             validators=[Length(1, 64),
                             Regexp(u'[A-Za-z0-9 ÁÉÍÓÚÂÊÎÔÛÃÕÇáéíóúâêîôûãõç]*$', 0)])

    ambiente = QuerySelectField('Ambiente', query_factory=lambda: Ambiente.query.all())

    intervalo_manutencao = IntegerField('Intervalo de Manutenção (Meses)',
                                        validators=[InputRequired(),
                                                    NumberRange(0)])
    
    em_uso = BooleanField('Em Uso')

    info_adicional = TextAreaField('Informações Adicionais')

    manutencoes = QuerySelectMultipleField('Manutenções',
                                           query_factory=lambda: Manutencao.query.all(),
                                           allow_blank=True)

    proxima_manutencao = DateField('Próxima Manutenção', widget=DatePickerWidget(),
                                   render_kw={'data-date-format': 'DD.MM.YYYY'},
                                   format='%d.%m.%Y',
                                   default=date.today())


# Criação de Manutenção
class FormCriarManutencao(FormBase):
    num_ordem_servico = IntegerField('Número da Ordem de Serviço',
                                     validators=[InputRequired(),
                                                 NumberRange(0)])

    data_abertura = DateField('Data de Abertura', widget=DatePickerWidget(),
                              render_kw={'data-date-format': 'DD.MM.YYYY'},
                              format='%d.%m.%Y',
                              default=date.today(),
                              validators=[InputRequired()])

    data_conclusao = DateFieldMod('Data de Conclusão', widget=DatePickerWidget(),
                               render_kw={'data-date-format': 'DD.MM.YYYY'},
                               format='%d.%m.%Y',
                               validators=[])

    tipo_manutencao = Select2Field('Tipo de Manutenção',
                                   choices=[('Preventiva', 'Preventiva'),
                                            ('Corretiva', 'Corretiva'),
                                            ('Troca', 'Troca'),
                                            ('Inicial', 'Inicial')])

    equipamento = QuerySelectField('Equipamento',
                                   query_factory=lambda: Equipamento.query.all())

    descricao_servico = TextAreaField('Descrição do Serviço')

    status = Select2Field('Status', choices=[('Aberta', 'Aberta'),
                                             ('Concluída', 'Concluída')])


    def __init__(self, *args, **kwargs):
        super(FormCriarManutencao, self).__init__(*args, **kwargs)

        # Caso, o id de um equipamento esteja presente na query string, trata-se
        # de uma manutenção inicial, logo, alguns campos são preenchidos automaticamente
        if request.args.get('id'):
            self.tipo_manutencao.data = 'Inicial'
            self.tipo_manutencao.render_kw = dict(disabled='disabled')

            self.equipamento.data = Equipamento.query.get(request.args.get('id'))
            self.equipamento.render_kw = dict(disabled='disabled')            

            self.status.data = 'Concluída'
            self.status.render_kw = dict(disabled='disabled')

    def validate_num_ordem_servico(self, field):
        if field.data != 0:
            if Manutencao.query.filter_by(num_ordem_servico=field.data).first():
                raise ValidationError('Manutenção já cadastrada.')

    def validate_data_conclusao(self, field):
        if self.status.data == 'Concluída':
            if field.data is None:
                raise ValidationError('Cadastre a data de conclusão.')

    def validate_status(self, field):
        if self.data_conclusao.data:
            if field.data == 'Aberta':
                raise ValidationError(
                    'Data de Conclusão cadastrada. Mude Status para "Concluída" ou deixe \
                     Data de Conclusão em branco.')


# Edição de Manutenção
class FormEditarManutencao(FormBase):
    num_ordem_servico = IntegerField('Número da Ordem de Serviço',
                                     validators=[InputRequired(),
                                                 NumberRange(0)])

    data_abertura = DateField('Data de Abertura', widget=DatePickerWidget(),
                              render_kw={'data-date-format': 'DD.MM.YYYY'},
                              format='%d.%m.%Y',
                              validators=[InputRequired()])

    data_conclusao = DateFieldMod('Data de Conclusão', widget=DatePickerWidget(),
                                  render_kw={'data-date-format': 'DD.MM.YYYY'},
                                  format='%d.%m.%Y')
    
    tipo_manutencao = Select2Field('Tipo de Manutenção',
                                   choices=[('Preventiva', 'Preventiva'),
                                            ('Corretiva', 'Corretiva'),
                                            ('Troca', 'Troca'),
                                            ('Inicial', 'Inicial')])

    equipamento = QuerySelectField('Equipamento',
                                   query_factory=lambda: Equipamento.query.all())

    descricao_servico = TextAreaField('Descrição do Serviço')

    status = Select2Field('Status', choices=[('Aberta', 'Aberta'),
                                             ('Concluída', 'Concluída')])


    def validate_data_conclusao(self, field):
        if self.status.data == 'Concluída':
            if field.data is None:
                raise ValidationError('Cadastre a data de conclusão.')

    def validate_status(self, field):
        if self.data_conclusao.data:
            if field.data == 'Aberta':
                raise ValidationError(
                    'Data de Conclusão cadastrada. Mude Status para "Concluída" ou deixe \
                     Data de Conclusão em branco.')

