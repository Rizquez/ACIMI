/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file alerts.js
 * @description Maneja la visualizacion y cierre de alertas personalizadas en la interfaz de usuario.
 * @param {string} msg - El mensaje que se mostrara en la alerta.
 */
function showAlert(msg) {
    const alertBox = document.getElementById("customized-alert")
    const alertText = document.getElementById("txt-alert")
    alertText.textContent = msg
    alertBox.style.display = 'block'

    // Asegurar que el boton cierre la alerta correctamente
    document.getElementById('btn-ok-alert').addEventListener("click", function() {
        closeAlert()
    })
}

/**
 * @file alerts.js
 * @description Cierra la alerta personalizada ocultando su contenedor.
 */
window.closeAlert = function () {
    const alertBox = document.getElementById("customized-alert")
    alertBox.style.display = 'none'
}

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/