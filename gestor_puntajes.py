import os
import pandas as pd

ARCHIVO_PUNTAJES = "puntajes.csv"

def inicializar_archivo():
    """Crea el archivo CSV con sus encabezados si aún no existe."""
    if not os.path.exists(ARCHIVO_PUNTAJES):
        with open(ARCHIVO_PUNTAJES, "w", encoding="utf-8") as archivo:
            archivo.write("Jugador,Juego,Puntaje\n")

def guardar_puntaje(jugador, juego, puntaje):
    """Agrega un nuevo registro al archivo CSV usando Pandas."""
    inicializar_archivo()
    
    # Leemos los puntajes actuales
    df = pd.read_csv(ARCHIVO_PUNTAJES)
    
    # Creamos una nueva fila con los datos de la partida
    nuevo_registro = pd.DataFrame([{
        "Jugador": jugador,
        "Juego": juego,
        "Puntaje": puntaje
    }])
    
    # Unimos y guardamos el archivo actualizado
    df_actualizado = pd.concat([df, nuevo_registro], ignore_index=True)
    df_actualizado.to_csv(ARCHIVO_PUNTAJES, index=False)

def cargar_puntajes():
    """Devuelve un DataFrame con todos los puntajes ordenados de mayor a menor."""
    inicializar_archivo()
    df = pd.read_csv(ARCHIVO_PUNTAJES)
    
    if not df.empty:
        df = df.sort_values(by="Puntaje", ascending=False).reset_index(drop=True)
    return df