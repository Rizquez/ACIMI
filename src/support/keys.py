# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
from typing import Union
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------------------------

class Templates:
    """
    Descripcion
    -----------
    Proporciona constantes que representan los valores a insertar dentro del las celdas de las tablas de `Excel` a descargar en formato de 
    plantilla por los usuarios de la aplicacion. Posee a su vez dos clases internas que hace referencia a cada tipo de plantilla generado.

    Detalles
    --------
    - Facilita el acceso a los registros durante la ejecucion mediante el uso de constantes claras y descriptivas.
    - Mejora la legibilidad y evita errores tipograficos en el manejo de claves.
    """

    ZERO = 0
    VALUE_EMPTY = 'Empty'

    @staticmethod
    def obtain_keys_template(cls: Union['Terciario', 'Residencial']) -> list:
        """
        Descripcion
        -----------
        Obtiene los valores almacenamos cada `key` de la clase que se le envie por parametro, esto lo logra realizando un filtrado sobre la 
        estructura del nombre de la clave y verificando si es un metodo; aunque esto ultimo no es posible sobre las clases actuales.

        Parametro
        ---------
        cls
            Clase sobre la que se quiere listar el valor de sus claves.

        Retorna
        -------
        - Lista ordenada con los valores almacenados en cada `key`.
        """
        return [value for key, value in vars(cls).items() if not key.startswith('__') and not key.startswith('_') and not callable(value)]
    
    class Terciario:
        """
        Descripcion
        -----------
        Proporciona constantes que representan los nombres de las columnas de la tabla que se generara dentro del documento `Excel` que 
        sirve de plantila para el calculo terciario.
        """

        PLANTA = 'planta'
        ESPACIO = 'espacio'
        SUPERFICIE = 'superficie (m2)'
        POTENCIA_TOTAL_CALEFACCION = 'potencia_total_calefaccion (W)'
        POTENCIA_TOTAL_REFRIGERACION = 'potencia_total_refrigeracion (W)'
        POTENCIA_CALEFACCION_SUPERFICIE = 'potencia_calefaccion_superficie (W/m2)'
        POTENCIA_REFRIGERACION_SUPERFICIE = 'potencia_refrigeracion_superficie (W/m2)'

    class Residencial:
        """
        Descripcion
        -----------
        Proporciona constantes que representan los nombres de las columnas de la tabla que se generara dentro del documento `Excel` que 
        sirve de plantila para el calculo residencial.
        """

        PLANTA = 'planta'
        ESPACIO = 'espacio'
        SUPERFICIE = 'superficie'
        
# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------