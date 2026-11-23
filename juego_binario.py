import random
import streamlit as st
import gestor_puntajes as gp

TOTAL_RONDAS = 5

# --- FUNCIONES DE LÓGICA PURA (CON RECURSIVIDAD) ---

def decimal_a_binario_recursivo(n):
    """Convierte un entero decimal a texto binario usando recursividad."""
    if n < 2:
        return str(n)
    return decimal_a_binario_recursivo(n // 2) + str(n % 2)

def binario_a_decimal_recursivo(binario):
    """Convierte un texto binario a entero decimal usando recursividad."""
    if len(binario) == 0:
        return 0
    primer_digito = int(binario[0])
    potencia = len(binario) - 1
    return primer_digito * (2 ** potencia) + binario_a_decimal_recursivo(binario[1:])

def es_binario_valido(texto):
    """Verifica que el texto contenga únicamente caracteres '0' y '1'."""
    if not texto:
        return False
    for caracter in texto:
        if caracter not in ("0", "1"):
            return False
    return True

def generar_pregunta():
    """Genera un número aleatorio y el tipo de conversión para la ronda actual."""
    st.session_state["bin_numero"] = random.randint(5, 63)
    st.session_state["bin_modo"] = random.choice(["dec_a_bin", "bin_a_dec"])

def iniciar_nueva_partida():
    """Reinicia las variables del quiz en la memoria de Streamlit."""
    st.session_state["bin_ronda"] = 1
    st.session_state["bin_puntaje"] = 0
    st.session_state["bin_terminado"] = False
    st.session_state["bin_guardado"] = False
    st.session_state["bin_feedback"] = ""
    generar_pregunta()

# --- INTERFAZ EN STREAMLIT ---

def mostrar_juego():
    st.header("💻 Desafío Binario ↔ Decimal")
    st.write(f"Responde {TOTAL_RONDAS} conversiones seguidas. Cada acierto vale **50 puntos**.")

    if "bin_ronda" not in st.session_state:
        iniciar_nueva_partida()

    if st.button("🔄 Reiniciar Desafío"):
        iniciar_nueva_partida()
        st.rerun()

    # Indicadores de progreso
    c1, c2 = st.columns(2)
    ronda_mostrada = min(st.session_state["bin_ronda"], TOTAL_RONDAS)
    c1.metric("Ronda", f"{ronda_mostrada} / {TOTAL_RONDAS}")
    c2.metric("Puntaje actual", st.session_state["bin_puntaje"])

    # Mostrar retroalimentación de la ronda anterior si existe
    if st.session_state["bin_feedback"]:
        if st.session_state["bin_feedback"].startswith("✅"):
            st.success(st.session_state["bin_feedback"])
        else:
            st.error(st.session_state["bin_feedback"])

    # Si el juego sigue activo
    if not st.session_state["bin_terminado"]:
        numero_dec = st.session_state["bin_numero"]
        numero_bin = decimal_a_binario_recursivo(numero_dec)

        if st.session_state["bin_modo"] == "dec_a_bin":
            st.info(f"Convierte el número decimal **{numero_dec}** a **binario**:")
            placeholder_txt = "Ejemplo: 10110"
        else:
            st.info(f"Convierte el número binario **{numero_bin}** a **decimal**:")
            placeholder_txt = "Ejemplo: 22"

        # Usar la ronda en la 'key' hace que la caja de texto se limpie sola en cada pregunta
        respuesta = st.text_input(
            "Tu respuesta:",
            placeholder=placeholder_txt,
            key=f"bin_input_{st.session_state['bin_ronda']}"
        )

        if st.button("Responder"):
            resp_limpia = respuesta.strip()

            if st.session_state["bin_modo"] == "dec_a_bin":
                if not es_binario_valido(resp_limpia):
                    st.warning("⚠️ Ingresa un número binario válido (solo 0 y 1).")
                    st.stop()
                
                # Comparamos usando nuestra función recursiva (así acepta ceros a la izquierda)
                if binario_a_decimal_recursivo(resp_limpia) == numero_dec:
                    st.session_state["bin_puntaje"] += 50
                    st.session_state["bin_feedback"] = f"✅ ¡Correcto! {numero_dec} en binario es {numero_bin}."
                else:
                    st.session_state["bin_feedback"] = f"❌ Incorrecto. {numero_dec} en binario es {numero_bin}."

            else:
                try:
                    valor_usuario = int(resp_limpia)
                except ValueError:
                    st.warning("⚠️ Ingresa un número entero válido.")
                    st.stop()

                if valor_usuario == numero_dec:
                    st.session_state["bin_puntaje"] += 50
                    st.session_state["bin_feedback"] = f"✅ ¡Correcto! {numero_bin} en decimal es {numero_dec}."
                else:
                    st.session_state["bin_feedback"] = f"❌ Incorrecto. {numero_bin} en decimal es {numero_dec}."

            # Avanzar de ronda o terminar el juego
            if st.session_state["bin_ronda"] >= TOTAL_RONDAS:
                st.session_state["bin_terminado"] = True
            else:
                st.session_state["bin_ronda"] += 1
                generar_pregunta()

            st.rerun()

    # Si ya completó las 5 rondas
    else:
        puntaje_final = st.session_state["bin_puntaje"]
        if puntaje_final >= 150:
            st.balloons()
            st.success(f"🎉 ¡Desafío completado! Puntaje final: **{puntaje_final} / {TOTAL_RONDAS * 50}**")
        else:
            st.warning(f"🏁 Desafío terminado. Puntaje final: **{puntaje_final} / {TOTAL_RONDAS * 50}**")

        if puntaje_final > 0:
            if not st.session_state["bin_guardado"]:
                nombre = st.text_input("Ingresa tu nombre para guardar tu récord:", key="bin_nombre")
                if st.button("Guardar puntaje", key="bin_btn_guardar"):
                    if nombre.strip() != "":
                        gp.guardar_puntaje(nombre.strip(), "Desafío Binario", puntaje_final)
                        st.session_state["bin_guardado"] = True
                        st.rerun()
                    else:
                        st.warning("Escribe un nombre válido.")
            else:
                st.info("✅ ¡Puntaje guardado en la Tabla de Posiciones!")