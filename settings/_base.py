# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
import binascii
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------------------------

class _SettingGlobal(object):
    """
    Actua como una plantilla para todas las demas clases se definen las 
    configuraciones segun cada entorno de ejecucion entornos de la aplicacion.
    """
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = binascii.hexlify(os.urandom(48)).decode()

class Development(_SettingGlobal):
    """
    Define la configuracion del entorno de `Desarollo`.
    """
    ENV = 'development'
    HOST = '127.0.0.1'
    PORT = '8080'
    DEBUG = True
    TESTING = True

class Production(_SettingGlobal):
    """
    Define la configuracion del entorno de `Produccion`.
    """
    ENV = 'production'
    HOST = '0.0.0.0'
    PORT = '8080'
    DEBUG = False
    TESTING = False

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------