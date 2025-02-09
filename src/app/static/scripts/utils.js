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

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/