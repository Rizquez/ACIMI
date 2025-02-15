# ACIMI - v0.2.0

## Contexto
En el campo de la ingeniería mecánica aplicada a edificaciones, el cálculo de instalaciones mecánicas para uso residencial y terciario es una tarea esencial que involucra múltiples factores técnicos. La automatización de estos cálculos reduce errores, mejora la eficiencia y optimiza el tiempo de los profesionales del sector.

Actualmente, muchos cálculos se realizan manualmente o mediante herramientas dispersas sin una solución integrada. ACIMI busca resolver esta problemática proporcionando una plataforma web que permite la entrada manual de datos o la carga de archivos Excel para automatizar estos cálculos.

## Descripcion del proyecto, caracteristicas y funcionalidades
__ACIMI__ proviene de las siglas en inglés _Automation of calculations in mechanical installations_, este proyecto es una aplicación web que permite a usuarios autenticados:
- Ingresar manualmente datos requeridos para cálculos de instalaciones mecánicas.
- Subir archivos Excel con datos estructurados para su procesamiento automático.
- Obtener cálculos de tipo residencial o terciario con base en los datos ingresados.
- Visualizar y descargar los resultados de los cálculos en diferentes formatos.

### Características principales
- __Autenticación y gestión de usuarios:__ Permite el acceso solo a usuarios registrados y autenticados.
- __Interfaz intuitiva:__ Diseñada para facilitar la carga manual y la gestión de archivos.
- __Automatización de cálculos:__ Procesamiento automatizado de cálculos específicos para instalaciones mecánicas.
- __Soporte para archivos Excel:__ Capacidad para leer, interpretar y procesar datos desde archivos Excel.
- __Gestión de cálculos para diferentes tipos de instalaciones:__ Cálculos especializados según las necesidades de instalaciones residenciales o terciarias.
- __Estructura modular:__ Organización del código en módulos bien definidos para facilitar el mantenimiento y escalabilidad del proyecto.

### Funcionalidad
La aplicación sigue un flujo lógico de operación:
- Un usuario autenticado accede a la plataforma.
- Puede optar por introducir datos manualmente o subir un archivo Excel con los datos necesarios.
- El sistema procesa la información, ejecutando los cálculos correspondientes.
- Se presentan los resultados en la interfaz, permitiendo su exportación si es necesario.
- El usuario puede gestionar su historial de cálculos y acceder a reportes generados.

## Variables de entorno
El proyecto requiere ciertas variables de entorno para su funcionamiento, estas variables deben estar definidas en un archivo `.env` en la raiz del proyecto.

La estructura esperada en el archivo `.env` es la siguiente:
```makefile
MSQL_USER = sql_user
MSQL_PASSWORD = sql_password
MSQL_HOST = sql_host
FLASK_ENV = execution_enviroment
```

> [!NOTE]
> Contacta a los responsables del proyecto para obtener los valores correctos de las variables de entorno.

## Estructura del proyecto
```
ACIMI/
├── design
│   └── singleton.py
├── settings
│   ├── _base.py
│   ├── constants.py
│   └── settings.py
├── src
│   ├── app
│   │   ├── routes/...
│   │   ├── static/...
│   │   └── templates/...
│   ├── services
│   └── utils
├── .env (local file)
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Instalacion y ejecucion
Antes de ejecutar este proyecto, asegurate de tener instalados los siguientes requisitos:
- Python version `3.11.x` o superior
- Dependencias externas ubicadas en el fichero `requirements.txt`

Ahora sigue estos pasos para configurar el entorno y ejecutar el proyecto:

1. Clona este repositorio (ssh):
```
git clone git@github.com:Rizquez/ACIMI.git
cd ACIMI
```

2. Crea un entorno virtual (opcional pero recomendado):
```
python -m venv venv
venv\Scripts\activate # En Linux/macOS usa `source venv/bin/activate`
```

3. Instala las dependencias:
```
pip install -r requirements.txt
```

Para ejecutar el proyecto, utiliza el siguiente comando:
```
python main.py
```

## Recursos adicionales

### Criterios de versionado semantico (x.xx.xxx)
El control de version se gestiona en el archivo `constants.py` ubicado en el directorio `settings`. A continuacion, se describen los criterios para cada numero de la version:
- __Mayor (x)__: Incrementa cuando hay cambios significativos que hacen que versiones anteriores sean incompatibles (e.g., cambios en la arquitectura o funcionalidades clave).
- __Menor (xx)__: Incrementa al agregar nuevas funcionalidades compatibles con la version anterior.
- __Parche (xxx)__: Incrementa al realizar correcciones de errores menores que no afectan la funcionalidad.

### Forward References (PEP 484)
El proyecto utiliza `Forward References` segun la `PEP 484`. Mediante el uso de `TYPE_CHECKING`, la importacion de una clase se realiza unicamente en tiempo de chequeo estatico de tipos (por ejemplo, con `mypy`). Durante la ejecucion, `TYPE_CHECKING` evalua como `False`, evitando la importacion real. Esto optimiza el rendimiento y permite referencias adelantadas a clases.
Ejemplo:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ModelBase

class NameClass:
    def name_method(self, model_base: 'ModelBase') -> None:
        pass
```

## Contribuciones
Este proyecto está cerrado para contribuciones ⛔.

No se aceptarán `pull requests` ni `issues` nuevos, tampoco se permite hacer `Fork` de este repositorio.

Gracias por su comprensión.

## Licencia
ACIMI se licencia bajo [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1).

Este software está protegido por derechos de autor. No se permite la redistribución, modificación o copia de este código en ninguna forma sin el permiso explícito del propietario. Cualquier uso no autorizado será perseguido bajo la ley aplicable.

© 2025 Pedro Rizquez Todos los derechos reservados.
