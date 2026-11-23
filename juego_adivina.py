import random
import streamlit as st
import gestor_puntajes as gp

# --- FUNCIONES DE LÓGICA PURA ---

def obtener_configuracion(dificultad):
    """Retorna (limite_maximo, max_intentos, puntos_base) según la dificultad."""
    match dificultad:
        case "Fácil (1 - 20)":
            return 20, 7, 100
        case "Medio (1 - 50)":
            return 50, 7, 200
        case "Difícil (1 - 100)":
            return 100, 6, 350

def evaluar_intento(intento, secreto):
    """Compara el número del jugador con el secreto."""
    if intento < secreto:
        return "menor"
    elif intento > secreto:
        return "mayor"
    else:
        return "correcto"

def calcular_puntaje(puntos_base, intentos_restantes):
    """Calcula el puntaje final premiando los intentos que sobraron."""
    return puntos_base + (intentos_restantes * 25)

def iniciar_nueva_partida(dificultad):
    """Reinicia las variables del juego en la memoria de Streamlit."""
    limite, max_intentos, puntos_base = obtener_configuracion(dificultad)
    st.session_state["adivina_dificultad"] = dificultad
    st.session_state["adivina_limite"] = limite
    st.session_state["adivina_secreto"] = random.randint(1, limite)
    st.session_state["adivina_intentos"] = max_intentos
    st.session_state["adivina_puntos_base"] = puntos_base
    st.session_state["adivina_terminado"] = False
    st.session_state["adivina_ganado"] = False
    st.session_state["adivina_guardado"] = False
    st.session_state["adivina_mensaje"] = ""

# --- INTERFAZ EN STREAMLIT ---

def mostrar_juego():
    st.header("🎯 Adivina el Número")
    st.write("Intenta descubrir el número secreto antes de quedarte sin intentos.")

    # Selector de dificultad y botón de reinicio
    col1, col2 = st.columns([3, 1])
    with col1:
        dificultad = st.selectbox(
            "Elige la dificultad:",
            ["Fácil (1 - 20)", "Medio (1 - 50)", "Difícil (1 - 100)"]
        )
    with col2:
        st.write("") # Espacio para alinear el botón
        st.write("")
        if st.button("🔄 Nuevo Juego"):
            iniciar_nueva_partida(dificultad)

    # Inicializar si es la primera vez que entra o si cambió la dificultad
    if "adivina_secreto" not in st.session_state or st.session_state["adivina_dificultad"] != dificultad:
        iniciar_nueva_partida(dificultad)

    # Mostrar estado actual
    st.metric(label="Intentos restantes", value=st.session_state["adivina_intentos"])

    # Si el juego sigue activo
    if not st.session_state["adivina_terminado"]:
        intento = st.number_input(
            f"Ingresa un número entre 1 y {st.session_state['adivina_limite']}:",
            min_value=1,
            max_value=st.session_state["adivina_limite"],
            step=1
        )

        if st.button("Probar número"):
            resultado = evaluar_intento(intento, st.session_state["adivina_secreto"])

            if resultado == "correcto":
                st.session_state["adivina_terminado"] = True
                st.session_state["adivina_ganado"] = True
                st.rerun()
            else:
                st.session_state["adivina_intentos"] -= 1
                if st.session_state["adivina_intentos"] == 0:
                    st.session_state["adivina_terminado"] = True
                    st.session_state["adivina_ganado"] = False
                elif resultado == "menor":
                    st.session_state["adivina_mensaje"] = f"⬆️ El número secreto es **mayor** que {intento}."
                else:
                    st.session_state["adivina_mensaje"] = f"⬇️ El número secreto es **menor** que {intento}."
                st.rerun()

        if st.session_state["adivina_mensaje"]:
            st.info(st.session_state["adivina_mensaje"])

    # Si el juego terminó
    else:
        if st.session_state["adivina_ganado"]:
            puntaje_final = calcular_puntaje(
                st.session_state["adivina_puntos_base"],
                st.session_state["adivina_intentos"]
            )
            st.balloons()
            st.success(f"🎉 ¡Ganaste! El número era **{st.session_state['adivina_secreto']}**. Tu puntaje es: **{puntaje_final}**")

            # Guardar puntaje en el CSV
            if not st.session_state["adivina_guardado"]:
                nombre = st.text_input("Ingresa tu nombre para guardar tu récord:")
                if st.button("Guardar puntaje"):
                    if nombre.strip() != "":
                        gp.guardar_puntaje(nombre.strip(), "Adivina el Número", puntaje_final)
                        st.session_state["adivina_guardado"] = True
                        st.rerun()
                    else:
                        st.warning("Por favor, escribe un nombre válido.")
            else:
                st.info("✅ ¡Puntaje guardado! Revísalo en la Tabla de Posiciones.")
        else:
            st.error(f"😢 Te quedaste sin intentos. El número secreto era **{st.session_state['adivina_secreto']}**.")