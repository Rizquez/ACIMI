/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file utils.js
 * @description Maneja la visibilidad del formulario terciario y restringe la entrada de numeros enteros mayor o igual a 0.
 */
document.addEventListener("DOMContentLoaded", function () {
    var tipoCalculoElement = document.getElementById("calculotipo")
    var formTerciario = document.getElementById("form-terciario")
    var inputNumber = document.querySelectorAll("#form-terciario input[type='number']")

    // Maneja la visibilidad del formulario terciario segun la seleccion del usuario
    if (tipoCalculoElement && formTerciario) {
        tipoCalculoElement.addEventListener("change", function () {
            formTerciario.style.display = this.value === "terciario" ? "block" : "none"
        })
    } else {
        console.error("Error: No se encontro el elemento con id 'calculotipo' o 'form-terciario'")
    }

    // Agrega validacion para restringir la entrada solo a enteros mayor o igual a 0
    if (inputNumber) {
        inputNumber.forEach(function (input) {
            input.addEventListener("input", function () {
                // Elimina caracteres no numericos y ajusta a un numero entero positivo
                var value = parseInt(this.value, 10)
                if (isNaN(value) || value < 0) {
                    this.value = "" // Borra el valor si es invalido
                } else {
                    this.value = value // Asegura que se almacene como un numero entero
                }
            })

            // Evita la entrada de caracteres no numericos
            input.addEventListener("keydown", function (event) {
                if (
                    !(
                        event.key >= "0" && event.key <= "9" || // Permitir numeros
                        event.key === "Backspace" || // Permitir borrar
                        event.key === "ArrowLeft" || event.key === "ArrowRight" || // Permitir navegacion con flechas
                        event.key === "Tab" || event.key === "Enter" // Permitir tabulacion y enter
                    )
                ) {
                    event.preventDefault() // Bloquea la tecla no permitida
                }
            })
        })
    }
})

/**
 * @file utils.js
 * @description Maneja la descarga de las plantillas al hacer clic en los elementos correspondientes evitando la recarga de la pagina.
 * @param {string} tipo - Tipo de plantilla a descargar ('terciario' o 'residencial').
 */
document.addEventListener("DOMContentLoaded", function () {
    
    function downloadTemplate(tipo) {
        var url = `/download_template/${tipo}`
        var link = document.createElement("a")
        link.href = url
        link.setAttribute("download", `Calculo_${tipo}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    // Asigna eventos de clic a los elementos de plantilla
    document.querySelectorAll(".template").forEach(function (elemento) {
        elemento.addEventListener("click", function () {
            var tipo = this.getAttribute("tipo")
            if (tipo) {
                downloadTemplate(tipo)
            }
        })
    })
})

/**
 * @file file_upload.js
 * @description Maneja la visualizacion del nombre del archivo seleccionado en el formulario de carga.
 */
document.addEventListener("DOMContentLoaded", function () {
    var fileInput = document.getElementById("fileupload")
    var fileNameDisplay = document.getElementById("file-name")

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = "Archivo seleccionado: " + fileInput.files[0].name
        } else {
            fileNameDisplay.textContent = "No se ha seleccionado ningun archivo"
        }
    })
})


/**
 * @file utils.js
 * @description Maneja la etiqueta `required` sobre los input del formulario que se activan unicamente para el calculo terciario.
 */
document.getElementById("calculotipo").addEventListener("change", function() {
    let formTerciario = document.getElementById("form-terciario")
    let isTerciario = this.value === "terciario"

    formTerciario.classList.toggle("hide", !isTerciario)

    // Obtener los campos dentro del formulario terciario
    let fields = formTerciario.querySelectorAll("input, select")
    
    // Agregar o quitar required dependiendo de si es visible
    fields.forEach(field => {
        if (isTerciario) {
            field.setAttribute("required", "required")
        } else {
            field.removeAttribute("required")
        }
    })
})

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/