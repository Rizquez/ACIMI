/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file terciario.js
 * @description Maneja la logica del formulario principal y validaciones en la entrada de datos.
 */
document.addEventListener("DOMContentLoaded", () => {

    // Metodo para controlar los checkbox
    handleCheckboxSelection()

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

            // Desactivamos las celdas en funcion del requerimiento
            updatePeopleFlow(selectedOption, row)
    
            // Si es sala_pci, habilitamos los inputs y asignamos placeholder y required
            setInputState(potencia_kw, isSalaPci, "Potencia (kW)")
            setInputState(potencia_hp, isSalaPci, "Potencia (HP)")
            setInputState(diametro_mm, isSalaPci, "Diametro (mm)")
    
            // Actualizamos (o eliminamos) la fila en la tabla dinamica segun el valor seleccionado
            updateDynamicRow(select, row, rowIndex)
        })
    })

    // Obtenemos referencias a los botones sobre la generacion de grupos e instanciamos el contador de grupos
    let groupCount = 0
    const addGroupButton = document.querySelector(".boton-grupo button:nth-child(1)")
    const removeGroupButton = document.querySelector(".boton-grupo button:nth-child(2)")

    // Inicialmente ocultamos el boton de eliminar y asignamos eventos a los botones
    removeGroupButton.style.display = "none"
    addGroupButton.addEventListener("click", addGroupColumn)
    removeGroupButton.addEventListener("click", removeLastGroupColumn)
  
    /**
     * @description Agrega los listeners necesarios a un input numerico para evitar caracteres o valores no deseados.
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
     * @description Configura el estado (habilitado/deshabilitado, placeholder y required) de un input.
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
     * @description Actualiza (o elimina) la fila correspondiente en la tabla dinamica (#dynamicTable) 
     * basandose en el valor del select y otros datos obtenidos de la fila actual y las tablas de alturas e inputs.
     * @param {HTMLSelectElement} select 
     * @param {HTMLElement} row - Fila (tr) donde se encuentra el select.
     * @param {string} rowIndex - El atributo data-index de la fila.
     */
    function updateDynamicRow(select, row, rowIndex) {
        const dynamicTableBody = document.querySelector("#dynamicTable tbody")
        const dynamicTableHead = document.querySelector("#dynamicTable thead tr")
        let dynamicRow = dynamicTableBody.querySelector(`tr[data-index="${rowIndex}"]`)

        // Si se selecciono un valor valido (distinto de "" y "0")
        if (select.value !== "" && select.value !== "0") {

            // Extraemos valores de la fila actual
            const espacioValue = row.querySelector("td:nth-child(1)").textContent.trim()
            const plantaValue = row.querySelector("td:nth-child(2)").textContent.trim()
            
            // Buscamos la altura de la planta en la tabla de alturas
            const heightsTable = document.querySelector("#heightsTable")
            let alturaPlantaValue = ''
            let alturaLibreValue = ''
            
            // Recorremos las filas del tbody de heightsTable
            heightsTable.querySelectorAll("tbody tr").forEach(tr => {
                const plantaCell = tr.querySelector("td")
                if (plantaCell && plantaCell.textContent.trim() === plantaValue) {
                    const inputs = tr.querySelectorAll("input[type='number']")
                    if (inputs.length >= 2) {
                    alturaPlantaValue = inputs[0].value
                    alturaLibreValue = inputs[1].value
                    }
                }
            })

            // Capturamos la superficie desde la tabla de inputs (inputsTable)
            const inputsTable = document.querySelector("#inputsTable")
            let superficieValue = ''
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
            let caudal = 0
            if (alturaPlantaValue > 0) {
                caudal =  select.value * alturaPlantaValue * superficieValue
            }
            else {
                caudal = select.value * alturaLibreValue * superficieValue
            }

            // Obtenemos el numero total de columnas en la tabla (incluyendo las dinamicas)
            const totalColumns = dynamicTableHead.querySelectorAll("th").length;


            // Generamos las celdas base (Espacio, Planta, Caudal)
            let rowContent = `
                <td>${espacioValue}</td>
                <td>${plantaValue}</td>
                <td>${Number((caudal).toFixed(2))}</td>
            `

            // Si hay más de 3 columnas, agregar checkboxes en las celdas adicionales
            for (let i = 4; i <= totalColumns; i++) {
                rowContent += `
                    <td>
                        <input type="checkbox" name="grupo_${i - 3}" value="agrupacion_${i - 3}">
                    </td>
                `
            }

            // Insertamos la fila con el contenido actualizado
            dynamicRow.innerHTML = rowContent
        } else {
            // Si se vuelve a la opcion por defecto, eliminamos la fila dinamica si existe
            if (dynamicRow) {
                dynamicRow.remove()
            }
        }
    }

    /**
     * @description Desactiva la celda de planta o caudal en la tabla Ocupacion & Caudal (Locales), segun se requiera.
     * @param {HTMLSelectElement} selectedOption 
     * @param {HTMLElement} row - Fila (tr) donde se encuentra el select.
     */
    function updatePeopleFlow(selectedOption, row) {
        const nPersonas = row.querySelector("input#n_personas")
        const caudal = row.querySelector("input#caudal_m3h") 

        // Lista de excepciones donde se aplica la restriccion
        const excepciones = ["almacences", "aseos", "lavanderias", "sala_cuadros", "sala_maquinas", "sala_pci", "sala_residuos"]
        
        // Si cambiamos a una opcion en `excepciones` y ambos inputs tienen valores, mostramos la alerta
        if (excepciones.includes(selectedOption.id) && nPersonas.value.trim() !== "" && caudal.value.trim() !== "") {
            showAlert(`
                Solo es posible indicar el numero de personas o el caudal para locales de tipo ${selectedOption.id.replace("_", " de ")}, 
                por favor ingrese nuevamente los datos para este tipo de local ⚠️`
            )
            caudal.value = ""
            nPersonas.value = "" 
            caudal.placeholder = "Caudal (m3/h)" 
            nPersonas.placeholder = "Nº Personas" 
        }

        // Verificamos si la opcion seleccionada esta en la lista de excepciones
        if (excepciones.includes(selectedOption.id)) {

            // Sobrescribimos el evento de `input` en Personas para que se reemplace si cambia la seleccion
            nPersonas.oninput = function () {
                if (nPersonas.value.trim() !== "") {
                    caudal.readOnly = true
                    caudal.value = ""
                    caudal.placeholder = ""
                }
                else {
                    caudal.readOnly = false 
                    caudal.placeholder = "Caudal (m3/h)" 
                }
            }

            // Sobrescribimos el evento de `input` en Caudal para que se reemplace si cambia la seleccion
            caudal.oninput = function () {
                if (caudal.value.trim() !== "") {
                    nPersonas.readOnly = true
                    nPersonas.value = "" 
                    nPersonas.placeholder = "" 
                } else {
                    nPersonas.readOnly = false 
                    nPersonas.placeholder = "Nº Personas" 
                }
            }

        // Si la opcion no esta en la lista de excepciones, habilitar ambos campos y eliminar eventos
        } else {
            nPersonas.readOnly = false
            caudal.readOnly = false
            nPersonas.oninput = null
            caudal.oninput = null
            nPersonas.placeholder = "Nº Personas"
            caudal.placeholder = "Caudal (m3/h)"
        }
    }
    
    /**
     * @description Agrega una nueva columna "Grupo N" en la tabla dinamica de agrupacion de locales por equipos mecanicos.
     */
    function addGroupColumn() {
        const dynamicTableHead = document.querySelector("#dynamicTable thead tr")
        const dynamicTableBody = document.querySelector("#dynamicTable tbody")
        groupCount++
    
        // Creamos y añadimos nueva columna en la cabecera
        const newHeader = document.createElement("th")
        newHeader.textContent = `Grupo ${groupCount}`
        dynamicTableHead.appendChild(newHeader)

        // Añadimos una celda en cada fila existente
        dynamicTableBody.querySelectorAll("tr").forEach(row => {
            const newCell = document.createElement("td")
            
            // Creamos el checkbox asignando un nombre unico basado en el grupo
            const checkbox = document.createElement("input")
            checkbox.type = "checkbox"
            checkbox.name = `grupo_${groupCount}`
            checkbox.value = `agrupacion_${groupCount}`
            
            // Insertamos el checkbox en la celda
            newCell.appendChild(checkbox)
            row.appendChild(newCell)
        })

        // Mostramos el boton de eliminar si hay grupos
        removeGroupButton.style.display = "inline-block"
    }

    /**
     * @description Elimina una nueva columna "Grupo N" en la tabla dinamica de agrupacion de locales por equipos mecanicos.
     */
    function removeLastGroupColumn() {

        // Verificamos si existen grupo para eliminar
        if (groupCount > 0) {
            const dynamicTableHead = document.querySelector("#dynamicTable thead tr")
            const dynamicTableBody = document.querySelector("#dynamicTable tbody")
            const headers = dynamicTableHead.querySelectorAll("th")
            const groupHeaders = Array.from(headers).filter(th => th.textContent.startsWith("Grupo "))

            // Verificamos si existen grupos en la cabecera de la tabla
            if (groupHeaders.length > 0) {

                // Eliminamos solo la ultima columna de grupo
                const lastGroupHeader = groupHeaders[groupHeaders.length - 1]
                dynamicTableHead.removeChild(lastGroupHeader)

                // Eliminamos la ultima celda de grupo en cada fila del cuerpo
                dynamicTableBody.querySelectorAll("tr").forEach(row => {
                    const cells = row.querySelectorAll("td")

                    // Controlamos para eliminar solo si hay suficientes celdas
                    if (cells.length >= headers.length) { 
                        row.removeChild(cells[cells.length - 1])
                    }
                })

                // Disminuimos la cantidad del grupo y ocultamos el boton de eliminar si ya no hay columnas de grupo
                groupCount--
                if (groupCount === 0) {
                    removeGroupButton.style.display = "none"
                }
            }
        }
    }

    /**
     * @description Controla que solo un checkbox pueda estar marcado a la vez en cada fila de la tabla.
     */
    function handleCheckboxSelection() {
        const dynamicTableBody = document.querySelector("#dynamicTable tbody")
        
        dynamicTableBody.addEventListener("change", function (event) {
            if (event.target.type === "checkbox") {
                const row = event.target.closest("tr")
                const checkboxes = row.querySelectorAll("input[type='checkbox']")

                if (event.target.checked) {
                    // Deshabilitamos los demas checkboxes en la fila
                    checkboxes.forEach(checkbox => {
                        if (checkbox !== event.target) {
                            checkbox.disabled = true
                        }
                    })
                } else {
                    // Reactivamos todos los checkboxes cuando se desmarca
                    checkboxes.forEach(checkbox => {
                        checkbox.disabled = false
                    })
                }
            }
        })
    }
})

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/  