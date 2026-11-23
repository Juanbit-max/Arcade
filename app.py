import streamlit as st
import gestor_puntajes as gp
import juego_adivina as ja
import juego_ordenar as jo
import juego_binario as jb
import juego_tesoro as jt

# Configuración de la página
st.set_page_config(
    page_title="Arcade Python",
    page_icon="🕹️",
    layout="centered"
)

# Menú lateral
st.sidebar.title("🕹️ Arcade Python")
st.sidebar.write("Selecciona una opción:")

opcion = st.sidebar.radio(
    "Navegación",
    [
        "Inicio",
        "1. Adivina el Número",
        "2. Reto de Ordenamiento",
        "3. Desafío Binario ↔ Decimal",
        "4. Caza del Tesoro",
        "🏆 Tabla de Posiciones"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.caption("Proyecto de Introducción a la Programación")

# Control de vistas con match-case
match opcion:
    case "Inicio":
        st.title("🕹️ Bienvenido al Arcade de Python")
        st.write("Pon a prueba tu lógica en cuatro minijuegos clásicos y compite por el primer lugar en la tabla de récords.")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Adivina el Número")
            st.write("Descubre el número secreto eligiendo entre tres niveles de dificultad antes de quedarte sin intentos.")

            st.subheader("💻 Desafío Binario ↔ Decimal")
            st.write("Ronda rápida de 5 conversiones entre sistema decimal y binario con lógica recursiva.")

        with col2:
            st.subheader("🔢 Reto de Ordenamiento")
            st.write("Ordena listas en el Modo Desafío o analiza y filtra tus propios números en el Modo Laboratorio.")

            st.subheader("🗺️ Caza del Tesoro")
            st.write("Explora un mapa 5×5 usando un radar de proximidad para encontrar el tesoro oculto.")

        st.divider()
        st.info("👈 Elige cualquier juego en el menú de la izquierda para comenzar.")

    case "1. Adivina el Número":
        ja.mostrar_juego()

    case "2. Reto de Ordenamiento":
        jo.mostrar_juego()

    case "3. Desafío Binario ↔ Decimal":
        jb.mostrar_juego()

    case "4. Caza del Tesoro":
        jt.mostrar_juego()

    case "🏆 Tabla de Posiciones":
        st.header("🏆 Mejores Puntajes")
        df_puntajes = gp.cargar_puntajes()

        if df_puntajes.empty:
            st.info("Aún no hay puntajes registrados. ¡Juega una partida para estrenar la tabla!")
        else:
            # Filtro dinámico por juego usando Pandas
            juegos_disponibles = ["Todos"] + sorted(df_puntajes["Juego"].unique().tolist())
            filtro = st.selectbox("Filtrar por minijuego:", juegos_disponibles)

            if filtro == "Todos":
                df_filtrado = df_puntajes
            else:
                df_filtrado = df_puntajes[df_puntajes["Juego"] == filtro].reset_index(drop=True)

            # Métricas resumen
            c1, c2, c3 = st.columns(3)
            c1.metric("Partidas registradas", len(df_filtrado))
            c2.metric("Puntaje más alto", int(df_filtrado["Puntaje"].max()))
            c3.metric("Líder actual", str(df_filtrado.iloc[0]["Jugador"]))

            # Mostrar tabla (empezando el índice visual en 1)
            df_mostrar = df_filtrado.copy()
            df_mostrar.index = range(1, len(df_mostrar) + 1)
            st.dataframe(df_mostrar, use_container_width=True)