/*------------------------------------------------------------- INICIO DEL FICHERO --------------------------------------------------------------*/

/**
 * @file terciario.js
 * @description
 */
document.addEventListener("DOMContentLoaded", function () {

    /**
     * @description Elementos del DOM necesarios para la manipulacion del formulario.
     */
    const numericInputs = document.querySelectorAll("table input[type='number']")
    const tipolocalSelects = document.querySelectorAll("select#tipolocal")

    /**
     * @description
     */
    numericInputs.forEach(input => {

        // Evento para evitar numeros negativos
        input.addEventListener("input", function () {
            let value = this.value

            // Impedimos numeros negativos eliminando el "-"
            if (value.startsWith("-")) {
                value = value.replace("-", "") 
            }
        })

        // Evento para evitar que el usuario ingrese un "-" o un "." directamente
        input.addEventListener("keydown", function (event) {
            if (event.key === "-" || event.key === ".") {
                event.preventDefault()
            }
        })

        // Evento para evitar el uso de decimales en el numero de personas
        if (input.id === "n_personas") {
            input.addEventListener("keydown", function (event){
                if (event.key === ",") {
                    event.preventDefault()
                }
            })
        }
    })

    /**
     * @description
     */
    tipolocalSelects.forEach(select => {

        // Buscamos la fila <tr> donde se encuentra este select
        const row = select.closest("tr")
        const rowIndex = row.getAttribute("data-index");

        // Dentro de esa fila, seleccionamos los inputs correspondientes
        const potencia_kw = row.querySelector("input#potencia_kw")
        const potencia_hp = row.querySelector("input#potencia_hp")
        const diametro_mm = row.querySelector("input#diametro_mm")

        // Inicialmente, deshabilitamos estos inputs (si existen)
        if (potencia_kw) {
            potencia_kw.disabled = true
            potencia_kw.required = false
        }
        if (potencia_hp) {
            potencia_hp.disabled = true
            potencia_hp.required = false
        }
        if (diametro_mm) {
            diametro_mm.disabled = true
            diametro_mm.required = false
        }

        // Añadimos un listener para el evento "change" del select
        select.addEventListener("change", function () {
            
            // Obtenemos los valores de las celdas
            const espacioValue = row.querySelector("td:nth-child(1)").textContent.trim()
            const plantaValue = row.querySelector("td:nth-child(2)").textContent.trim()
            
            // Seleccionamos el <tbody> de la tabla dinamica
            const dynamicTableBody = document.querySelector("#dynamicTable tbody")

            // Buscamos si ya existe una fila para este indice
            let dynamicRow = dynamicTableBody.querySelector(`tr[data-index="${rowIndex}"]`)

            // Obtenemos la opcion seleccionada (la propiedad id se asigna a cada <option> en el HTML)
            const selectedOption = select.options[select.selectedIndex]

            // Si se selecciono la opcion sala_pci, habilitamos los inputs y los marcamos como requeridos
            // Si se selecciona cualquier otro valor, se deshabilitan y se quita la condicion "required"
            if (selectedOption && selectedOption.id === "sala_pci") {
                if (potencia_kw) {
                    potencia_kw.disabled = false
                    potencia_kw.required = true
                    potencia_kw.placeholder = "Potencia (kW)"
                }
                if (potencia_hp) {
                    potencia_hp.disabled = false
                    potencia_hp.required = true
                    potencia_hp.placeholder = "Potencia (HP)"
                }
                if (diametro_mm) {
                    diametro_mm.disabled = false
                    diametro_mm.required = true
                    diametro_mm.placeholder = "Diametro (mm)"
                }
            } else {
                if (potencia_kw) {
                    potencia_kw.disabled = true
                    potencia_kw.required = false
                    potencia_kw.placeholder = ""
                }
                if (potencia_hp) {
                    potencia_hp.disabled = true
                    potencia_hp.required = false
                    potencia_hp.placeholder = ""
                }
                if (diametro_mm) {
                    diametro_mm.disabled = true
                    diametro_mm.required = false
                    diametro_mm.placeholder = ""
                }
            }

            // Si se selecciono un valor valido (diferente de la opcion por defecto)
            if (select.value !== "" && select.value !== "0") {

                // Si la fila no existe, la creamos
                if (!dynamicRow) {
                    dynamicRow = document.createElement("tr")
                    dynamicRow.setAttribute("data-index", rowIndex)
                    dynamicTableBody.appendChild(dynamicRow)
                }

                // Actualizamos el contenido de la fila
                dynamicRow.innerHTML = `<td>${espacioValue}</td><td>${plantaValue}</td><td>${select.value}</td>`
            } else {
                // Si se ha vuelto a la opcion por defecto, eliminamos la fila dinamica si existe
                if (dynamicRow) {
                    dynamicRow.remove()
                }
            }
        })
    })
})

/*---------------------------------------------------------------- FIN DEL FICHERO --------------------------------------------------------------*/