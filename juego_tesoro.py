import random
import numpy as np
import streamlit as st
import gestor_puntajes as gp

TAMANO = 5
MAX_INTENTOS = 8

# Diccionario que traduce los códigos numéricos de la matriz NumPy a emojis
SIMBOLOS = {
    0: "⬜",  # Casilla sin explorar
    1: "🌊",  # Agua (vacío)
    2: "💎"   # Tesoro encontrado
}

# --- FUNCIONES DE LÓGICA PURA ---

def crear_tablero(tamano):
    """Crea una matriz 2D de ceros usando NumPy."""
    return np.zeros((tamano, tamano), dtype=int)

def generar_tesoro(tamano):
    """Devuelve una tupla (fila, columna) con la ubicación secreta del tesoro."""
    fila = random.randint(0, tamano - 1)
    col = random.randint(0, tamano - 1)
    return (fila, col)

def calcular_distancia(coord_usuario, coord_tesoro):
    """Calcula la distancia Manhattan entre dos tuplas de coordenadas."""
    return abs(coord_usuario[0] - coord_tesoro[0]) + abs(coord_usuario[1] - coord_tesoro[1])

def obtener_pista(distancia):
    """Retorna una pista de radar según qué tan cerca esté el tesoro."""
    if distancia == 1:
        return "🔥 ¡Ardiendo! El tesoro está justo al lado (a 1 casilla)."
    elif distancia == 2:
        return "🌡️ ¡Caliente! Estás muy cerca."
    elif distancia <= 4:
        return "🌤️ Tibio... vas por buen camino."
    else:
        return "❄️ Frío, el tesoro está lejos de aquí."

def iniciar_nueva_partida():
    """Reinicia la matriz NumPy, la tupla del tesoro y el set de casillas visitadas."""
    st.session_state["tes_tablero"] = crear_tablero(TAMANO)
    st.session_state["tes_ubicacion"] = generar_tesoro(TAMANO)
    st.session_state["tes_visitadas"] = set()
    st.session_state["tes_intentos"] = MAX_INTENTOS
    st.session_state["tes_terminado"] = False
    st.session_state["tes_ganado"] = False
    st.session_state["tes_guardado"] = False
    st.session_state["tes_pista"] = "Haz clic en cualquier casilla del mapa para empezar a buscar."

# --- INTERFAZ EN STREAMLIT ---

def mostrar_juego():
    st.header("🗺️ Caza del Tesoro")
    st.write(f"Hay un tesoro oculto en este mapa de {TAMANO}×{TAMANO}. Tienes **{MAX_INTENTOS} intentos** para encontrarlo usando el radar.")

    if "tes_tablero" not in st.session_state:
        iniciar_nueva_partida()

    if st.button("🔄 Nuevo Mapa"):
        iniciar_nueva_partida()
        st.rerun()

    tablero = st.session_state["tes_tablero"]
    visitadas = st.session_state["tes_visitadas"]
    ubicacion_tesoro = st.session_state["tes_ubicacion"]

    # Operación con NumPy para contar cuántas casillas siguen sin explorar (valor 0)
    casillas_restantes = int(np.count_nonzero(tablero == 0))

    c1, c2 = st.columns(2)
    c1.metric("Intentos restantes", st.session_state["tes_intentos"])
    c2.metric("Casillas sin explorar", casillas_restantes)

    # Mostrar pista del radar
    if not st.session_state["tes_terminado"]:
        st.info(st.session_state["tes_pista"])

    # Dibujar la matriz 2D como una cuadrícula de botones
    for fila in range(TAMANO):
        columnas = st.columns(TAMANO)
        for col in range(TAMANO):
            coord = (fila, col)  # Tupla de coordenada actual
            simbolo = SIMBOLOS[tablero[fila, col]]
            deshabilitado = st.session_state["tes_terminado"] or (coord in visitadas)

            if columnas[col].button(
                simbolo,
                key=f"tes_celda_{fila}_{col}",
                use_container_width=True,
                disabled=deshabilitado
            ):
                # Registrar la tupla en el set de visitadas
                visitadas.add(coord)

                if coord == ubicacion_tesoro:
                    tablero[fila, col] = 2
                    st.session_state["tes_terminado"] = True
                    st.session_state["tes_ganado"] = True
                else:
                    tablero[fila, col] = 1
                    st.session_state["tes_intentos"] -= 1
                    dist = calcular_distancia(coord, ubicacion_tesoro)
                    st.session_state["tes_pista"] = obtener_pista(dist)

                    if st.session_state["tes_intentos"] == 0:
                        # Revelar dónde estaba el tesoro al perder
                        f_tes, c_tes = ubicacion_tesoro
                        tablero[f_tes, c_tes] = 2
                        st.session_state["tes_terminado"] = True
                        st.session_state["tes_ganado"] = False

                st.rerun()

    # Resultado final y guardado de puntaje
    if st.session_state["tes_terminado"]:
        if st.session_state["tes_ganado"]:
            puntaje_final = 100 + (st.session_state["tes_intentos"] * 40)
            st.balloons()
            st.success(f"🎉 ¡Encontraste el tesoro en la coordenada {ubicacion_tesoro}! Puntaje: **{puntaje_final}**")

            if not st.session_state["tes_guardado"]:
                nombre = st.text_input("Ingresa tu nombre para guardar tu récord:", key="tes_nombre")
                if st.button("Guardar puntaje", key="tes_btn_guardar"):
                    if nombre.strip() != "":
                        gp.guardar_puntaje(nombre.strip(), "Caza del Tesoro", puntaje_final)
                        st.session_state["tes_guardado"] = True
                        st.rerun()
                    else:
                        st.warning("Escribe un nombre válido.")
            else:
                st.info("✅ ¡Puntaje guardado en la Tabla de Posiciones!")
        else:
            st.error(f"😢 Te quedaste sin intentos. El tesoro estaba escondido en la coordenada **{ubicacion_tesoro}**.")