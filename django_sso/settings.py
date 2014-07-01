"""
Django settings for django_sso project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from os import path
import saml2
BASEDIR = path.dirname(path.abspath(__file__))

PATH_XMLSEC = '/usr/local/share/doc/xmlsec1'
MAIN_URL = 'localhost:8000'
try:
    from local import *
except ImportError:
    # No local settings which is fine
    pass

AUTH_USER_MODEL = 'accounts.CustomUser'

REST_PROFILE_MODULE = AUTH_USER_MODEL

ACCOUNT_ACTIVATION_DAYS = 3

#registration api, this could be used for i.e. Wordpress Theme
REST_REGISTRATION_BACKEND = 'registration.backends.default.views.RegistrationView'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '11lm=jpqi-44+5hvyp4ng@00gnd&$-ggh1xp_7$fu46x$r&15z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    )
AUTHENTICATION_BACKENDS = (
      'django.contrib.auth.backends.ModelBackend',
      'djangosaml2.backends.Saml2Backend',
  )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
         'rest_framework.authentication.SessionAuthentication',
    )
}

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosaml2',
    'django_sso',
    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'rest_auth',
    'accounts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_sso.urls'

WSGI_APPLICATION = 'django_sso.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'



SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': PATH_XMLSEC,

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'http://%s/saml2/metadata/' % MAIN_URL,

  # directory with attribute mapping
  #'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'name': 'Federated Django sample SP',
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ('http://%s/saml2/acs/' % MAIN_URL,
                   saml2.BINDING_HTTP_POST),
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  ('http://%s/saml2/ls/' % MAIN_URL,
                   saml2.BINDING_HTTP_REDIRECT),
                  ],
              },

           # attributes that this project need to identify a user
          'required_attributes': ['uid'],

           # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              'http://sp.zimmermanzimmerman.com/simplesaml/saml2/idp/metadata.php': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'http://sp.zimmermanzimmerman.com/simplesaml/saml2/idp/SSOService.php',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'http://sp.zimmermanzimmerman.com/simplesaml/saml2/idp/SingleLogoutService.php',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [path.join(BASEDIR, 'remote_metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': path.join(BASEDIR, 'privatekey.pem'),  # private part should be key?
  'cert_file': path.join(BASEDIR, 'publickey.cer'),  # public part

  # own metadata settings
  'contact_person': [
      {'given_name': 'Siem',
       'sur_name': 'Vaessen',
       'company': 'Zimmerman&Zimmerman',
       'email_address': 'siem@zimmermanzimmerman.nl',
       'contact_type': 'CTO'},
      {'given_name': 'Berjan',
       'sur_name': 'Bruens',
       'company': 'Zimmerman&Zimmerman',
       'email_address': 'berjan@zimmermanzimmerman.nl',
       'contact_type': 'technical'},
      ],
  # you can set multilanguage information here
  'organization': {
      'name': [('Zimmerman&Zimmerman', 'nl'), ('Zimmerman&Zimmerman', 'en')],
      'display_name': [('Zimmerman&Zimmerman', 'nl'), ('Zimmerman&Zimmerman', 'en')],
      'url': [('http://www.zimmermanzimmerman.nl', 'nl'), ('http://zimmermanzimmerman.nl', 'en')],
      },
  'valid_for': 24,  # how long is our metadata valid
  }
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename' : 'django_sso.log',
        },
    },
    'loggers': {
        'djangosaml2': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local import *
except ImportError:
    # No local settings which is fine
    pass