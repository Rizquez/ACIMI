/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file utils.js
 * @description Maneja la activacion de alertas para el usuario de manera global (se emplea en el fichero base.html).
 */
document.addEventListener('DOMContentLoaded', function() {
    if (window.flaskMessages && window.flaskMessages.length > 0) {
      showAlert(window.flaskMessages)
    }
})

/**
 * @description Maneja la descarga de plantillas segun el tipo seleccionado.
 */
document.querySelectorAll(".template").forEach(element => {
  element.addEventListener("click", function () {
    const tipo = this.getAttribute("tipo")
    if (tipo) downloadTemplate(tipo)
  })
})

/**
* @description Descarga una plantilla de calculo basada en el tipo seleccionado.
* @param {string} tipo - Tipo de plantilla a descargar ("terciario" o "residencial").
*/
function downloadTemplate(tipo) {
  const url = `/download_template/${tipo}`
  const link = document.createElement("a")
  link.href = url
  link.setAttribute("download", `Plantilla_calculo_${tipo}.xlsx`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/