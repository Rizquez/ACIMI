# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
import openpyxl.utils
import openpyxl.worksheet.table
import openpyxl.worksheet
import pandas as pd
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

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------