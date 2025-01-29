# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING
import openpyxl.styles

if TYPE_CHECKING:
    from openpyxl import Workbook
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------------------------

class ProcessExcel:
    """
    Descripcion
    -----------
    Reune internamente un conjunto de metodos especializados para realizar operaciones avanzadas y personalizadas sobre archivos de `Excel` con 
    funciones complejas, utilizando la libreria `openpyxl`.

    Detalles
    --------
    - El objetivo es facilitar tareas comunes como la manipulacion de documentos de `Excel` de manera eficiente.
    - La informacion detallada acerca del alcance de aplicacion de cada metodo, se encuentra internamente en su respectiva documentacion.
    """

    @staticmethod
    def adjust_columns(wb: 'Workbook', sheet_name: str, justify: str = 'center') -> 'Workbook':
        """
        Descripcion
        -----------
        Ajusta el ancho de las columnas de todas las tablas en una hoja de Excel.

        Analizando cada columna en la hoja especificada, calcula el ancho necesario para contener los valores mas largos de las celdas y ajusta el 
        ancho de las columnas en consecuencia, alinea tambien, el texto de las celdas segun la justificacion especificada.

        Detalles
        --------
        - Si una celda no contiene un valor (es `None`), no afecta el calculo del ancho de la columna.
        - El ancho ajustado incluye un margen adicional para mejorar la visibilidad de los datos.

        Parametros
        ----------
        wb
            Objeto Workbook de `openpyxl` que representa el archivo de Excel a modificar.

        sheet_name
            Nombre de la hoja de Excel donde se encuentran las tablas cuyas columnas se ajustaran.

        h 
            Tipo de alineacion horizontal para las celdas, valores comunes incluyen: `left` | `center` | `right`.

        Retorna
        -------
        - El mismo objeto Workbook, pero con las columnas ajustadas en la hoja especificada.
        """
        # Longitud a sumar sobre la anchura calculada para obtener un poco mas de olgura sobre cada columnaa
        PLUS_LENGTH = 8

        # Entramos por cada columna de la tabla en la hoja y establecemos a 0 el ancho 
        # de la columna, para poder realizar el calculo real de la anchura que debe poseer
        for column in wb[sheet_name].columns:
            length_max = 0

            # Listamos e iteramos sobre todas las celdas de cada columna
            # Calculando y ajustando el ancho de la columna en funcion del maximo ancho de las celdas
            lst_cells = [cell for cell in column]
            for cell in lst_cells:
                try:
                    length_cell = len(str(cell.value))
                    if length_cell > length_max:
                        length_max = length_cell
                    cell.alignment = openpyxl.styles.Alignment(horizontal=justify)
                except AttributeError:
                    print(f"Excel: Could not calculate the width of {cell.value} in cell {cell.coordinate} for sheet {sheet_name}")

            adjusted_width = (length_max + PLUS_LENGTH)
            wb[sheet_name].column_dimensions[column[0].column_letter].width = adjusted_width

        return wb
    
# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------