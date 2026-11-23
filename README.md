# 🕹️ Arcade de Minijuegos en Python

Aplicación interactiva desarrollada en Python y Streamlit como proyecto para la materia **Introducción a la Programación (ECMC1008)**.

## 🎮 Minijuegos incluidos
1. **Adivina el Número:** Tres niveles de dificultad, límite de intentos y cálculo de puntaje.
2. **Reto de Ordenamiento:** Modo desafío con puntaje y modo laboratorio con algoritmo de ordenamiento burbuja, *slicing* y filtro de pares/impares.
3. **Desafío Binario ↔ Decimal:** Quiz de 5 rondas con conversiones implementadas mediante funciones recursivas.
4. **Caza del Tesoro:** Tablero interactivo 5×5 construido con matrices 2D de NumPy, tuplas, sets y diccionarios.
5. **Tabla de Posiciones:** Persistencia de puntajes en formato `.csv` con filtrado y estadísticas usando Pandas.

## ⚙️ Instalación y ejecución
1. Instalar las dependencias:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Ejecutar la aplicación:
   ```bash
   python -m streamlit run app.py
   ```