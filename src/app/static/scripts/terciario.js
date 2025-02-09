/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file terciario.js
 * @description Maneja la logica del formulario principal y validaciones en la entrada de datos.
 */
document.addEventListener("DOMContentLoaded", () => {

    // Asignamos listeners a los inputs numericos
    const numericInputs = document.querySelectorAll("table input[type='number']")
    numericInputs.forEach(addNumericInputListeners)
  
    // Asignamos listeners a los selects con id tipolocal
    const tipolocalSelects = document.querySelectorAll("select#tipolocal")
    tipolocalSelects.forEach(select => {
        const row = select.closest("tr")
        const rowIndex = row.getAttribute("data-index")
    
        // Seleccionamos los inputs de potencia y diametro (pueden no existir)
        const potencia_kw = row.querySelector("input#potencia_kw")
        const potencia_hp = row.querySelector("input#potencia_hp")
        const diametro_mm = row.querySelector("input#diametro_mm")
    
        // Inicialmente, deshabilitamos y quitamos la obligatoriedad de estos inputs
        setInputState(potencia_kw, false, "")
        setInputState(potencia_hp, false, "")
        setInputState(diametro_mm, false, "")
    
        // Listener para el evento change del select
        select.addEventListener("change", () => {

            // Obtenemos la opcion seleccionada
            const selectedOption = select.options[select.selectedIndex]
            const isSalaPci = selectedOption && selectedOption.id === "sala_pci"
    
            // Si es sala_pci, habilitamos los inputs y asignamos placeholder y required
            setInputState(potencia_kw, isSalaPci, "Potencia (kW)")
            setInputState(potencia_hp, isSalaPci, "Potencia (HP)")
            setInputState(diametro_mm, isSalaPci, "Diametro (mm)")
    
            // Actualizamos (o eliminamos) la fila en la tabla dinamica segun el valor seleccionado
            updateDynamicRow(select, row, rowIndex)
        })
    })
  
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

            // Si el id es "n_personas", tambien evitamos la coma
            if ((input.id === "n_personas" || input.id === "plazas_coches" || input.id === "plazas_motos") && event.key === ",") {
                event.preventDefault()
            }
        })
    }
  
    /**
     * Configura el estado (habilitado/deshabilitado, placeholder y required) de un input.
     * @param {HTMLInputElement} input 
     * @param {boolean} enable - Si es true, habilita el input y asigna el placeholder de lo contrario, lo deshabilita.
     * @param {string} placeholder - Texto a asignar como placeholder cuando se habilita.
     */
    function setInputState(input, enable, placeholder) {
        if (!input) return
        input.disabled = !enable
        input.required = enable
        input.placeholder = enable ? placeholder : ""
    }
  
    /**
     * Actualiza (o elimina) la fila correspondiente en la tabla dinamica (#dynamicTable)
     * basandose en el valor del select y otros datos obtenidos de la fila actual y las tablas de alturas e inputs.
     * @param {HTMLSelectElement} select 
     * @param {HTMLElement} row - Fila (tr) donde se encuentra el select.
     * @param {string} rowIndex - El atributo data-index de la fila.
     */
    function updateDynamicRow(select, row, rowIndex) {
        const dynamicTableBody = document.querySelector("#dynamicTable tbody")
        let dynamicRow = dynamicTableBody.querySelector(`tr[data-index="${rowIndex}"]`)
    
        // Si se selecciono un valor valido (distinto de "" y "0")
        if (select.value !== "" && select.value !== "0") {

            // Extraemos valores de la fila actual
            const espacioValue = row.querySelector("td:nth-child(1)").textContent.trim()
            const plantaValue = row.querySelector("td:nth-child(2)").textContent.trim()
    
            // Buscamos la altura de la planta en la tabla de alturas
            const heightsTable = document.querySelector("#heightsTable")
            let alturaPlantaValue = ''
            
            // Recorremos las filas del tbody de heightsTable
            heightsTable.querySelectorAll("tbody tr").forEach(tr => {
                const plantaCell = tr.querySelector("td")
                if (plantaCell && plantaCell.textContent.trim() === plantaValue) {
                    const inputs = tr.querySelectorAll("input[type='number']")
                    if (inputs.length >= 2) {
                    alturaPlantaValue = inputs[0].value
                    }
                }
            })

            // Capturamos la superficie desde la tabla de inputs (inputsTable)
            const inputsTable = document.querySelector("#inputsTable");
            let superficieValue = '';
            inputsTable.querySelectorAll("tbody tr").forEach(tr => {
                const tds = tr.querySelectorAll("td")

                // Se comparan la primera celda (espacio) y segunda celda (planta)
                if (tds[0].textContent.trim() === espacioValue && tds[1].textContent.trim() === plantaValue) {

                    // Se asume que la septima celda contiene el input de la superficie
                    const superficieInput = tds[6].querySelector("input")
                    if (superficieInput) {
                        superficieValue = superficieInput.value
                    }
                }
            })
  
            // Creamos la fila dinamica si no existe
            if (!dynamicRow) {
                dynamicRow = document.createElement("tr")
                dynamicRow.setAttribute("data-index", rowIndex)
                dynamicTableBody.appendChild(dynamicRow)
            }
  
            // Calculamos el caudal (nota: se asume que select.value y alturaPlantaValue son numericos)
            const caudal = select.value * alturaPlantaValue * superficieValue
            dynamicRow.innerHTML = `
                <td>${espacioValue}</td>
                <td>${plantaValue}</td>
                <td>${caudal}</td>
            `
        } else {
            // Si se vuelve a la opcion por defecto, eliminamos la fila dinamica si existe
            if (dynamicRow) {
                dynamicRow.remove()
            }
        }
    }
})
/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/  