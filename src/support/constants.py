# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
import openpyxl.worksheet.table
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------------------------

ACIMI_VERSION = '0.0.0'
"""Version de la aplicacion."""

FOLDER_ROOT = '\\'.join(item for item in os.path.dirname(os.path.abspath(__file__)).split('\\')[:-2])
"""Carpeta raiz donde se ejecuta la aplicacion."""

FOLDER_TEMP_UPLOAD = os.path.join(FOLDER_ROOT, 'src', 'app', 'static', 'temp', 'upload')
"""Carpeta temporal para almacenar los archivos cargados a la aplicacion."""

FOLDER_TEMP_DOWNLOAD = os.path.join(FOLDER_ROOT, 'src', 'app', 'static', 'temp', 'download')
"""Carpeta temporal para almacenar los archivos que pueden ser descargados desde la aplicacion."""

STYLE_EXCEL = openpyxl.worksheet.table.TableStyleInfo(name='TableStyleMedium12', showFirstColumn=False, showLastColumn=False)
"""Estilo asignado a las tablas que existiran dentro de los documentos Excel creados por la aplicacion."""

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------