# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
import openpyxl.utils
import openpyxl.worksheet.table
import openpyxl.worksheet
import pandas as pd
from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
from src.support import Templates
from src.support import STYLE_EXCEL
from src.utils._xlsx import ProcessExcel
# -------------------------------------------------------------------------------------------------------------------------------------------------

class PdUtils(pd.DataFrame):
    """
    Descripcion
    -----------
    Extiende de la clase `pandas.DataFrame`, reuniendo internamente un conjunto de metodos especializados para realizar operaciones 
    avanzadas y personalizadas con DataFrames, asi como gestionar operaciones de lectura y escritura en documentos de `Excel` utilizando 
    `pandas` y `openpyxl`.

    Detalles
    --------
    - El objetivo es facilitar tareas comunes como la insercion, modificacion y eliminacion de datos de manera eficiente.
    - La informacion detallada acerca del alcance de aplicacion de cada metodo, se encuentra internamente en su respectiva documentacion.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def template_xlsx(tipo: str) -> 'PdUtils':
        """
        Descripcion
        -----------
        Genera un DataFrame a partir de uno datos bases segun el tipo de parametro indicado.

        Parametros
        ----------
        tipo
            Tipo calculo bajo el cual se creara el DataFrame, se espera como valor: `terciario` o `residencial`.

        Retorna
        -------
        - DataFrame de con los datos base segun el tipo de calculo.
        """
        if tipo.lower() == 'terciario':
            dct_data = {
                Templates.Terciario.ESPACIO: [Templates.VALUE_EMPTY],
                Templates.Terciario.PLANTA: [Templates.VALUE_EMPTY],
                Templates.Terciario.POTENCIA_REFRIGERACION_SUPERFICIE: [Templates.ZERO],
                Templates.Terciario.POTENCIA_TOTAL_REFRIGERACION: [Templates.ZERO],
                Templates.Terciario.POTENCIA_CALEFACCION_SUPERFICIE: [Templates.ZERO],
                Templates.Terciario.POTENCIA_TOTAL_CALEFACCION: [Templates.ZERO],
                Templates.Terciario.SUPERFICIE: [Templates.ZERO]
            }

        elif tipo.lower() == 'residencial':
            dct_data = {
                Templates.Residencial.ESPACIO: [Templates.VALUE_EMPTY],
                Templates.Residencial.PLANTA: [Templates.VALUE_EMPTY],
                Templates.Residencial.SUPERFICIE: [Templates.ZERO]
            }

        else:
            raise ValueError(f"El tipo de calculo {tipo} no se encuentra contemplato por el metodo `template_xlsx`")
        
        return PdUtils(dct_data)
    
    def save_excel(self, file: str, table_name: str, sheet_name: str, mode: str, float_format: str) -> None:
        """
        Descripcion
        -----------
        Crea o actualiza una tabla en un archivo `Excel` a partir de un `DataFrame`.

        Detalles
        --------
        - La tabla abarca desde la celda `A1` hasta el tamaño dinamico del `DataFrame`.
        - Ajusta automaticamente el ancho de las columnas y alinea las celdas.

        Parametros
        ----------
        file
            Ruta del archivo `Excel` donde se creara o actualizara la tabla.

        table_name
            Nombre que tendra la tabla en el documento.

        sheet_name
            Nombre de la hoja donde se insertara la tabla.

        mode
            Modo de escritura
                `'w'`: Sobrescribe o crea un archivo nuevo.
                `'a'`: Agrega nuevas hojas al archivo existente.

        float_format
            Formato de los valores flotantes en el archivo `Excel` (ejemplo: `%.2f`).

        Lanza
        -----
        `FileNotFoundError`
            Si el documento no existe y se intenta usar el modo `'a'`.

        `ValueError`
            Si los nombres de la tabla, hoja o documento contienen caracteres no validos.
        """
        # Primero debemos almacenar el DataFrame en un fichero Excel
        with pd.ExcelWriter(file, mode=mode) as writer:
            self.to_excel(writer, sheet_name=sheet_name, index=False, float_format=float_format, na_rep=0)

        # Abrimos el fichero excel para poder trabajar sobre el 
        wb = openpyxl.load_workbook(filename=file)

        # Con el DataFrame podemos instanciar y dimensionar la tabla
        dimension = f'A1:{openpyxl.utils.get_column_letter(self.shape[1])}{len(self)+1}'
        table = openpyxl.worksheet.table.Table(displayName=table_name, ref=dimension)
        table.tableStyleInfo = STYLE_EXCEL

        # Una vez instanciada la tabla, la insertamos en el documento y ajustamos el ancho de sus columnas
        wb[sheet_name].add_table(table)
        wb = ProcessExcel.adjust_columns(wb, sheet_name)
        wb.save(file)

    @staticmethod
    def read_table(file: str, table: str) -> 'PdUtils':
        """
        Descripcion
        -----------
        Lee una tabla especifica de un archivo `Excel` y la convierte en un `DataFrame`.

        Parametros
        ----------
        file
            Ruta absoluta del archivo de `Excel`.

        table
            Nombre de la tabla que se desea leer.

        Retorna
        -------
        - Contenido de la tabla en formato `DataFrame`.

        Lanza
        -----
        `FileNotFoundError`
            Si el archivo de `Excel` especificado no existe.

        `ValueError`
            Si la tabla especificada no se encuentra en el archivo.
        """
        # Controlamos la extraccion de datos desde el documento
        try: 
            # Abrimos el documento indicando las configuraciones de lectura que deseamos
            wb = openpyxl.load_workbook(filename=file, read_only=False, data_only=True)
            sheet_with_table = None
            tbl = None

            # Ahora vamos a iterar sobre cada hoja del libro
            for sheetname in wb.sheetnames:
                sheet = wb[sheetname]

                # Por cada hoja vamos a comprobrar si la tabla que buscamos existe dentro de esta hoja
                # Ya que pueden haber muchisimas tablas sobre una misma hoja
                # Y en el caso de obtenerla, extraeremos la tabla y almacenaremos la hoja, rompiendo posteriormente el bucle
                if table in sheet.tables:
                    tbl = sheet.tables[table]
                    sheet_with_table = sheet
                    break
            
            # En caso de nunca conseguirla arrojaremos un error
            else:
                raise ValueError(f"La tabla `{table}` no se encontra en el documento `{file}`")
            
            # Sobre la tabla obtenida anteriormente, vamos a localizar sus dimensiones
            # Y sobre las dimensiones, los datos almacenamos
            tbl_range = tbl.ref
            data = sheet_with_table[tbl_range]

            # Iterando sobre los datos podremos obtener el valor en cada celda
            content = [[cell.value for cell in row] for row in data]

            # Del contenido de las celdas separamos el nombre de las columans del valor en cada celda de cada fila e instanciamos el DataFrame
            header = content[0]
            rest = content[1:]
            df = PdUtils(rest, columns=header)

        finally:
            wb.close()
        
        return df
    
    @classmethod
    def validate_xlsx(self, file: 'FileStorage', table: str) -> tuple[bool, str]:
        """
        Descripcion
        -----------
        Realiza comprobaciones sobre el archivo `Excel` para verificar si cumple con los criterios para poder ser utilizado en la aplicacion.

        Parametros
        ----------
        file
            Archivo `Excel` cargado a la aplicacion a traves de Flask.

        table
            Nombre de la tabla que se va a buscar dentro del documento `Excel`.

        Retorna 
        -------
        - `True` si el archivo es valido o `False` en caso contrario.
        - Mensaje relacionado con la validacion que finalizo la ejecucion del metodo.
        """
        # Vamos a instanciar un diccionario que nos permitira acceder de forma rapida a la verificacion de las columnas de la tabla
        dct_access = {
            'Tabla_terciario': Templates.Terciario,
            'Tabla_residencial': Templates.Residencial
        }

        # Leemos el archivo Excel en el buffer de memoria
        file_buffer = BytesIO(file.read())
        file_buffer.seek(0)

        # Controlaremos la lectura de los datos sobre el documento, ya que es lo primero a validar, que exista la tabla
        try:
            df = self.read_table(file_buffer, table)

            # Verificamos si la tabla contiene datos
            if df.empty:
                return False, f'El documento `{file.filename}` no contiene datos en la tabla `{table}` 🔍'

            # Verificamos si todas las columnas existen
            if not set(Templates.obtain_keys_template(dct_access[table])).issubset(df.columns):
                return False, f'La tabla `{table}` no contiene todas las columnas necesarias para el calculo, por favor utilice la plantilla 🧐'

        # Si no se existe la tabla, lo indicaremos
        except ValueError:
            return False, f'La tabla `{table}` no existe dentro del documento `{file.filename}` 🔍'
            
        # Si todas las comprobaciones son correctas, retornamos un simple true y un ok
        return True, 'Ok'

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------