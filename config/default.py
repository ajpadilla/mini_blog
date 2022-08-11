from os.path import abspath, dirname, join

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

MEDIA_DIR = join(BASE_DIR, 'media')
POST_IMAGE_DIR = join(MEDIA_DIR, 'posts')

SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False

#App enviroments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

ITEMS_PER_PAGE = 3

# Configuración del email
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 587
MAIL_USERNAME = 'postmaster@sandboxc71e97aa21694467937db14038d23c6a.mailgun.org'
MAIL_PASSWORD = 'cd6ad8a33f67cd9b3408295ec31489f5'
DONT_REPLY_FROM_EMAIL = '(Juanjo, juanjo@j2logo.com)'
ADMINS = ('juanjo@j2logo.com', )
MAIL_USE_TLS = False
MAIL_USE_SSL = False

