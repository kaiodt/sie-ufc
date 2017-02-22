# coding: utf-8


################################################################################
## SIE - UFC
################################################################################
## Arquivo de Configuração
################################################################################


import os

# Diretório base
basedir = os.path.abspath(os.path.dirname(__file__))


########## Classes de Configuração ##########

# Configuração Geral
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'w\xc4\x1d\xfc\xaf\xab.\x03a\x02!\x87#p\nH\xcb\xd4\x86yV\x90Z\x89'  # !!!!!!!

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'kaiodtr@gmail.com'      # !!!!!!!

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'sie.ufc@gmail.com'  # !!!!!!!
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'InfoEletricas'      # !!!!!!!
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or 'SIE-UFC <sie.ufc@gmail.com>'

    MAPBOX_MAP_ID = 'mapbox.streets'
    MAPBOX_ACCESS_TOKEN = \
        'pk.eyJ1IjoibHVjYXNzbSIsImEiOiJjaW05cDlmMXYwMDFidzhtM3JzN291dzZqIn0.WC0WGjp2FzN0VNOZ3JHjnQ'

        
# Configuração de Desenvolvimento
class ConfigDesenvolvimento(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
      'postgresql://sie_ufc_admin:sie_ufc@localhost/dev_sie_ufc'

# Configuração de Teste
class ConfigTeste(Config):
    TESTING = True


# Configuração de Produção
class ConfigProducao(Config):
    pass


########## Dicionário para Seleção de Configuração ##########

modos_configuracao = {
    'desenvolvimento': ConfigDesenvolvimento,
    'teste': ConfigTeste,
    'producao': ConfigProducao,

    'padrao': ConfigDesenvolvimento
}

