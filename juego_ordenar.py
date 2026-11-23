import random
import streamlit as st
import gestor_puntajes as gp

# --- FUNCIONES DE LÓGICA PURA ---

def ordenar_burbuja(lista, ascendente=True):
    """Ordena una lista usando el algoritmo de burbuja (bucles for, range e indexación)."""
    resultado = lista.copy()
    n = len(resultado)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if ascendente:
                if resultado[j] > resultado[j + 1]:
                    resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
            else:
                if resultado[j] < resultado[j + 1]:
                    resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
    return resultado

def filtrar_pares_impares(lista):
    """Separa los números enteros en dos listas usando el método append()."""
    pares = []
    impares = []
    for num in lista:
        if num % 2 == 0:
            pares.append(num)
        else:
            impares.append(num)
    return pares, impares

def texto_a_lista_enteros(texto):
    """Convierte un texto como '5, 2, 9' en una lista de enteros [5, 2, 9]."""
    if not texto.strip():
        return None
    partes = texto.split(",")
    numeros = []
    for elemento in partes:
        try:
            numeros.append(int(elemento.strip()))
        except ValueError:
            return None
    return numeros

def iniciar_desafio():
    """Genera una nueva lista aleatoria para el modo desafío."""
    st.session_state["ord_lista"] = random.sample(range(1, 100), 6)
    st.session_state["ord_tipo"] = random.choice(["Menor a Mayor", "Mayor a Menor"])
    st.session_state["ord_resuelto"] = False
    st.session_state["ord_guardado"] = False

# --- INTERFAZ EN STREAMLIT ---

def mostrar_juego():
    st.header("🔢 Reto de Ordenamiento")
    
    tab1, tab2 = st.tabs(["🏆 Modo Desafío (Con Puntaje)", "🧪 Modo Laboratorio (Tus Números)"])

    # ---------------- PESTAÑA 1: DESAFÍO ----------------
    with tab1:
        if "ord_lista" not in st.session_state:
            iniciar_desafio()

        if st.button("🔄 Generar nueva lista"):
            iniciar_desafio()
            st.rerun()

        st.subheader(f"Ordena estos números de **{st.session_state['ord_tipo']}**:")
        
        # Mostramos la lista de forma visual
        texto_lista = "  |  ".join([str(n) for n in st.session_state["ord_lista"]])
        st.info(f"**Lista desordenada:**  {texto_lista}")

        if not st.session_state["ord_resuelto"]:
            respuesta_usuario = st.text_input(
                "Escribe los números ordenados separados por comas (ejemplo: 4, 12, 25, ...):"
            )

            if st.button("Verificar orden"):
                lista_usuario = texto_a_lista_enteros(respuesta_usuario)
                
                if lista_usuario is None:
                    st.warning("⚠️ Por favor, ingresa solo números enteros separados por comas.")
                else:
                    es_ascendente = (st.session_state["ord_tipo"] == "Menor a Mayor")
                    lista_correcta = ordenar_burbuja(st.session_state["ord_lista"], ascendente=es_ascendente)

                    if lista_usuario == lista_correcta:
                        st.session_state["ord_resuelto"] = True
                        st.rerun()
                    else:
                        st.error("❌ El orden no es correcto. ¡Revisa bien e inténtalo de nuevo!")
        else:
            puntaje = 150
            st.balloons()
            st.success(f"🎉 ¡Excelente! Ordenaste la lista perfectamente. Ganaste **{puntaje} puntos**.")

            if not st.session_state["ord_guardado"]:
                nombre = st.text_input("Tu nombre para el récord:", key="ord_nombre")
                if st.button("Guardar puntaje", key="ord_btn_guardar"):
                    if nombre.strip() != "":
                        gp.guardar_puntaje(nombre.strip(), "Reto de Ordenamiento", puntaje)
                        st.session_state["ord_guardado"] = True
                        st.rerun()
                    else:
                        st.warning("Escribe un nombre válido.")
            else:
                st.info("✅ ¡Puntaje guardado en la Tabla de Posiciones!")

    # ---------------- PESTAÑA 2: LABORATORIO ----------------
    with tab2:
        st.write("Ingresa tus propios números para ordenarlos, filtrarlos y analizarlos.")
        entrada = st.text_input("Números separados por comas:", placeholder="Ejemplo: 45, 12, 8, 99, 23, 4")
        orden = st.radio("Tipo de orden:", ["Ascendente (Menor a Mayor)", "Descendente (Mayor a Menor)"], horizontal=True)

        if st.button("Procesar lista"):
            numeros = texto_a_lista_enteros(entrada)
            
            if numeros is None or len(numeros) == 0:
                st.warning("⚠️ Ingresa al menos un número entero válido separado por comas.")
            else:
                es_asc = (orden == "Ascendente (Menor a Mayor)")
                ordenada = ordenar_burbuja(numeros, ascendente=es_asc)
                pares, impares = filtrar_pares_impares(ordenada)

                st.success(f"**Lista ordenada:** {ordenada}")

                # Estadísticas usando columnas
                c1, c2, c3 = st.columns(3)
                c1.metric("Mínimo", min(ordenada))
                c2.metric("Máximo", max(ordenada))
                c3.metric("Promedio", round(sum(ordenada) / len(ordenada), 2))

                # Slicing (primeros 3 elementos) y filtros
                st.write(f"**Top 3 (slicing `[:3]`):** {ordenada[:3]}")
                st.write(f"**Números pares:** {pares if pares else 'Ninguno'}")
                st.write(f"**Números impares:** {impares if impares else 'Ninguno'}")