/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file residencial.js
 * @description Maneja la logica del formulario principal y validaciones en la entrada de datos.
 */
document.addEventListener("DOMContentLoaded", () => {

    // Asignamos listeners a los inputs numericos
    const numericInputs = document.querySelectorAll("table input[type='number']")
    numericInputs.forEach(addNumericInputListeners)

    /**
     * Agrega los listeners necesarios a un input numerico para evitar caracteres o valores no deseados.
     * @param {HTMLInputElement} input 
     */
    function addNumericInputListeners(input) {

        // Evita que se ingresen numeros negativos (quita el "-" si se pega o se ingresa)
        input.addEventListener("input", function () {
            if (this.value.startsWith("-")) {
                this.value = this.value.replace("-", "")
            }
        })
  
        // Evita que se ingrese "-" o "." desde el teclado
        input.addEventListener("keydown", function (event) {
            if (event.key === "-" || event.key === ".") {
                event.preventDefault()
            }
        })
    }
})

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/  