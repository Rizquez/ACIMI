# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
from flask import Flask, render_template, redirect, send_file, request
from dotenv import load_dotenv
load_dotenv(override=False)
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
from src.support import FOLDER_ROOT
from src.utils import PdUtils
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Instanciamos la app de Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Necesitamos instanciar el directorio temp donde se almacenaran todos los archivos con los que trabajaremos, y si no existe lo creamos
FOLDER_TEMP = os.path.join(FOLDER_ROOT, 'src', 'app', 'static', 'temp')
os.makedirs(FOLDER_TEMP, exist_ok=True)

@app.route('/')
def home():
    """
    Descripcion
    -----------
    Ruta raiz de la aplicacion.

    Renderiza el fichero `home.html`.

    Retorna
    -------
    - Documento `home.html` renderizado.
    """
    return render_template('home.html')

@app.route('/download_template/<tipo>')
def download_template(tipo):
    """
    Descripcion
    -----------
    Ruta para realizar la descarga de las plantillas de `Excel` para realizar los calculos, estas plantillas poseen el mismo formato que se 
    espera tengan los fichero que se recibiran para el calculo.

    Parametros
    ----------
    tipo
        Tipo calculo bajo el cual se creara la plantilla `Excel`, se espera como valor: `terciario` o `residencial`.

    Retorna
    -------
    - Documento `Excel` descargado sobre la carpeta `descargas` del ordenador del usuario.
    """
    # Definimos el nombre de la plantilla en funcion del tipo
    filename = f'Calculo_{tipo}.xlsx'

    # Sobre el nombre de la plantilla definimos el nombre de la ruta del documento dentro del directorio temporal
    filepath = os.path.join(FOLDER_TEMP, filename)

    # Instanciamos el dataframe que servira de plantilla y lo almacenamos como documento excel
    df = PdUtils.template_xlsx(tipo)
    df.save_excel(filepath, f'Tabla_{tipo}', f'Hoja_{tipo}', 'w', '%.2f')

    return send_file(filepath, as_attachment=True, download_name=filename, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.route('/submit_data_initial', methods=['POST'])
def submit_data_initial():
    """
    Descripcion
    -----------
    Ruta que recibe los datos del formulario inicial y procesa la informacion.

    Detalles
    --------
    - Esta ruta de momento no realiza ningun control sobre el documento enviado.

    Retorna
    -------
    - Renderizado de `terciario.html` o `residencial.html` en funcion del tipo de calculo solicitado.
    """
    # Capturamos los datos del formulario
    num_referencia = request.form.get('num_referencia')
    nombre_proyecto = request.form.get('nombre_proyecto')
    propiedad = request.form.get('propiedad')
    autor = request.form.get('autor')
    calculotipo = request.form.get('calculotipo').lower()

    # Si es terciario, capturamos los datos adicionales
    ida = request.form.get('ida') if calculotipo == 'terciario' else None
    plantas_parking = request.form.get('plantas_parking') if calculotipo == 'terciario' else None
    zonas_sobrepresion = request.form.get('zonas_sobrepresionar') if calculotipo == 'terciario' else None

    # Manejamos archivo Excel si existe y lo almacenamos en el directorio temporal
    file = request.files.get('fileupload')
    if file:
        file.save(os.path.join(FOLDER_TEMP, f'upload_{file.filename}'))

    return render_template('terciario.html') if calculotipo == 'terciario' else render_template('residencial.html')

@app.errorhandler(404)
def error_handler(error):
    """
    Descripcion
    -----------
    Ruta para controlar el error 404.

    Detalles
    --------
    - Este metodo puede controlar todos los errores que se le indiquen mendiate `@app.errorhandler(xxx)`.

    Parametros
    ----------
    error
        Tipo de error capturado por el errorhandler.

    Retorna
    -------
    - Redireccionamiento a la ruta `/error`.
    """
    return redirect('/error')

@app.route('/error')
def error():
    """
    Descripcion
    -----------
    Ruta para renderizar el fichero `error.html`.

    Retorna
    -------
    - Fichero `error.html` renderizado.
    """
    return render_template('error.html')

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------