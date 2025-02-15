# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
import os
from io import BytesIO
from flask import Flask, render_template, redirect, send_file, request, flash
from dotenv import load_dotenv
load_dotenv(override=False)
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
from src.utils import PdUtils
# -------------------------------------------------------------------------------------------------------------------------------------------------

# REFERENCIA AL FICHERO LOG (INFO/WARNING/ERROR)
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Se referencian aqui!
# -------------------------------------------------------------------------------------------------------------------------------------------------

# CREACION DE LA(S) CLASE(S) / FUNCIONES GENERALES
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Instanciamos la app de Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')

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
    Ruta para realizar la descarga de las plantillas de `Excel` para realizar los calculos, estas plantillas poseen 
    el mismo formato que se espera tengan los fichero que se recibiran para el calculo.

    Parametros
    ----------
    tipo
        Tipo calculo bajo el cual se creara la plantilla `Excel`, se espera como valor: `terciario` o `residencial`.

    Retorna
    -------
    - Documento `Excel` descargado sobre la carpeta `descargas` del ordenador del usuario.
    """
    # Definimos el nombre de la plantilla en funcion del tipo
    filename = f'Plantilla_calculo_{tipo}.xlsx'

    # Instanciamos el dataframe que servira de plantilla y lo almacenamos como documento excel usando un buffer en 
    # memoria para guardar el archivo
    df = PdUtils.template_excel(tipo)
    save_buffer = df.save_excel(tipo, tipo, 'w', '%.2f')

    # Si hubo un error al generar el documento excel, enviamos un mensaje y redireccionamos a la raiz
    if save_buffer is None:
        flash(f"No es posibles obtener la plantilla para el calculo {tipo} en este momento, por favor contacte con soporte 🔧")
        return redirect('/')

    return send_file(
        save_buffer, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        as_attachment=True, 
        download_name=filename
    )

@app.route('/submit_data_initial', methods=['GET', 'POST'])
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
    # Controlamos el acceso directo a esta ruta y redireccionamos a la raiz
    # Solo mostramos el mensaje si NO viene de un formulario valido
    if request.method == 'GET':
        if not request.referrer or ('/submit_data_initial' not in request.referrer and '/' not in request.referrer):
            flash("No es posible acceder directamente a la ruta a la que he intentado ingresar, debe completar primero el formulario ⛔")
        return redirect('/')
    
    # Condicional para evaluar el envio del formulario
    elif request.method == 'POST' and request.form.get('calculotipo'):
    
        # Capturamos los datos del formulario
        num_referencia = request.form.get('num_referencia')
        nombre_proyecto = request.form.get('nombre_proyecto')
        propiedad = request.form.get('propiedad')
        autor = request.form.get('autor')
        calculotipo = request.form.get('calculotipo')

        # Si es terciario, capturamos los datos adicionales
        ida = request.form.get('ida') if calculotipo == 'terciario' else None
        plantas_parking = request.form.get('plantas_parking') if calculotipo == 'terciario' else None
        zonas_sobrepresionar = request.form.get('zonas_sobrepresionar') if calculotipo == 'terciario' else None

        # Extraemos el documento Excel enviado en el formulario
        file = request.files.get('fileupload')

        # Leemos el archivo Excel en el buffer de la memoria de la aplicacion
        buffer_file = BytesIO(file.read())

        # Reiniciamos el puntero al inicio del archivo para poder reutilizarlo
        buffer_file.seek(0)

        # Capturamos el nombre del archivo para facilidad de envio de mensajes al usuario
        file_name = file.filename
        
        # Debemos controlar la posibilidad de que los usuarios envien un documento que no tenga la estructura esperada, para ello, 
        # sobre el documento enviado a traves del formulario vamos a realizar una serie de validaciones antes de ir a los calculos
        # El front ya se encarga de aceptar unicamente fichero .xlsx, ahora comprobaremos si existe la tabla y las columnas en funcion 
        # del tipo de calculo que se quiera realizar
        isValid, msgValid = PdUtils.validate_xlsx(buffer_file, file_name, calculotipo)

        # Reiniciamos el puntero nuevamente tras la validacion
        buffer_file.seek(0)

        # Si los datos son validos, almacenamos el documento en el directorio temporal de cargas y redireccionamos al html correspondiente 
        # haciendo envio de los datos necesario segun cada html
        if isValid:
            dct_data = PdUtils.read_table(buffer_file, file_name, calculotipo).to_dict(orient='list')
            lst_plantas = list(sorted(set(dct_data['planta'])))

            # Renderizado para el calculo terciario
            if calculotipo == 'terciario':
                return render_template(
                    'terciario.html', 
                    dct_data = dct_data, 
                    lst_plantas = lst_plantas,
                    dct_zonas = {
                        'parking': int(plantas_parking),
                        'sobrepresion': int(zonas_sobrepresionar)
                    }
                )
            
            # Renderizado para el calculo residencial
            else:
                return render_template(
                    'residencial.html',
                    dct_data = dct_data, 
                    lst_plantas = lst_plantas
                )
        
        # En caso contrario, enviamos el mensaje obtenido de la validacion al front
        else:
            flash(msgValid)
            return redirect(request.url)
        
    # Por defecto siempre redireccionaremos a la pagina principal
    else:
        return redirect('/')

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
# FIN DEL FICHERO :)
# -------------------------------------------------------------------------------------------------------------------------------------------------