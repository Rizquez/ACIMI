# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS (EXTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
from typing import Any
# -------------------------------------------------------------------------------------------------------------------------------------------------

# LIBRERIAS (INTERNAS)
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Se importan aqui!
# -------------------------------------------------------------------------------------------------------------------------------------------------

# REFERENCIA AL FICHERO LOG (INFO/WARNING/ERROR)
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Se referencian aqui!
# -------------------------------------------------------------------------------------------------------------------------------------------------

# # CREACION DE LA(S) CLASE(S) / FUNCIONES GENERALES
# -------------------------------------------------------------------------------------------------------------------------------------------------

class Singleton(type):
    """
    Summary
    -------
    Metaclase para implementar el patron de diseño `Singleton`.

    Details
    -------
    - Esta metaclase garantiza que cualquier clase que la utilice solo tenga una unica instancia durante el ciclo de vida del algoritmo.
    - Si se intenta crear una nueva instancia de una clase que utiliza esta metaclase, se devolvera la instancia existente.
    - Todas las instancias creadas de las clases que usan `Singleton` se almacenan en un diccionario interno, donde la clave es la clase y el 
    valor es la instancia unica asociada.
    """
    # Diccionario para almacenar la relacion entre clases e instancias unicas
    _instances = {}

    def __call__(cls, *args: tuple, **kwargs: dict) -> Any:
        """
        Summary
        -------
        Controla la creacion de instancias para implementar el patron `Singleton`.

        Details
        -------
        - Este metodo sobrescribe el comportamiento predeterminado del metodo especial `__call__` para asegurarse de que, independientemente de 
        cuantas veces se intente crear una instancia de una clase que hereda de `Singleton`, siempre se devuelva la misma instancia.

        Notes
        -----
        - `__call__` es un metodo especial en Python que permite que una clase o metaclase se comporte como si fuera una funcion.
        - En este caso el metodo `__call__` se utiliza para personalizar la logica de creacion de instancias.
        
        Parameters
        ----------
        args
            Argumentos posicionales que se pasaran al constructor de la clase base.

        kwargs
            Argumentos con nombre que se pasaran al constructor de la clase base.

        Returns 
        -------
        - Instancia unica existente de la clase que hereda de `Singleton`.
        """
        # Controlamos si la instancia de la clase no existe, lo que nos permite crearla y almacenarla de forma referenciada
        # En caso contrario retornamos directamente la instancia existente de la clase indicada
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO :)
# -------------------------------------------------------------------------------------------------------------------------------------------------