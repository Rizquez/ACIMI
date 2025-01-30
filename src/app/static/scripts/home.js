/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file home.js
 * @description Maneja la logica del formulario principal, validaciones y descargas de plantillas.
 */
document.addEventListener("DOMContentLoaded", function () {

    /**
     * Elementos del DOM necesarios para la manipulacion del formulario
     */
    const tipoCalculoElement = document.getElementById("calculotipo")
    const formTerciario = document.getElementById("form-terciario")
    const inputNumberFields = document.querySelectorAll("#form-terciario input[type='number']")
    const fileInput = document.getElementById("fileupload")
    const fileNameDisplay = document.getElementById("file-name")
    const form = document.getElementById("main-form")
    
    /**
     * Maneja la visibilidad del formulario terciario y el atributo 'required'.
     * Se activa cuando el usuario selecciona "terciario" en el menu desplegable.
     */
    tipoCalculoElement.addEventListener("change", function () {
        const isTerciario = this.value === "terciario"
        formTerciario.classList.toggle("hide", !isTerciario)
        formTerciario.querySelectorAll("input, select").forEach(field => {
            isTerciario ? field.setAttribute("required", "required") : field.removeAttribute("required")
        })
    })

    /**
     * Aplica restricciones en los campos de numero para aceptar solo enteros positivos.
     */
    inputNumberFields.forEach(input => {
        input.addEventListener("input", restrictToPositiveIntegers)
        input.addEventListener("keydown", preventNonNumericInput)
    })

    /**
     * Restringe la entrada de caracteres en los campos numericos a valores enteros positivos.
     * @param {Event} event - Evento de entrada en el campo de texto.
     */
    function restrictToPositiveIntegers(event) {
        let value = parseInt(event.target.value, 10)
        event.target.value = isNaN(value) || value < 0 ? "" : value
    }

    /**
     * Previene la entrada de caracteres no numericos en los campos de numeros.
     * @param {KeyboardEvent} event - Evento de teclado.
     */
    function preventNonNumericInput(event) {
        const allowedKeys = ["Backspace", "ArrowLeft", "ArrowRight", "Tab", "Enter"]
        if (!(/[0-9]/.test(event.key) || allowedKeys.includes(event.key))) {
            event.preventDefault()
        }
    }

    /**
     * Muestra el nombre del archivo seleccionado para cargar.
     */
    fileInput.addEventListener("change", function () {
        fileNameDisplay.textContent = fileInput.files.length > 0 
            ? "Archivo seleccionado: " + fileInput.files[0].name 
            : "No se ha seleccionado ningun archivo"
    })

    /**
     * Maneja la validacion antes del envio del formulario.
     * Previene el envio si no se ha seleccionado un archivo.
     */
    form.addEventListener("submit", function (event) {
        if (!validateFileSelection()) {
            event.preventDefault()
        }
    })

    /**
     * Valida que se haya seleccionado un archivo antes de enviar el formulario.
     * @returns {boolean} - Retorna `true` si el archivo esta seleccionado, `false` si falta.
     */
    function validateFileSelection() {
        if (fileInput.files.length === 0) {
            showAlert("Debe subir el documento Excel base con los datos de entrada antes de enviar el formulario 📑")
            return false
        }
        return true
    }

    /**
     * Maneja la descarga de plantillas segun el tipo seleccionado.
     */
    document.querySelectorAll(".template").forEach(element => {
        element.addEventListener("click", function () {
            const tipo = this.getAttribute("tipo")
            if (tipo) downloadTemplate(tipo)
        })
    })

    /**
     * Descarga una plantilla de calculo basada en el tipo seleccionado.
     * @param {string} tipo - Tipo de plantilla a descargar ("terciario" o "residencial").
     */
    function downloadTemplate(tipo) {
        const url = `/download_template/${tipo}`
        const link = document.createElement("a")
        link.href = url
        link.setAttribute("download", `Calculo_${tipo}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }
})

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/