# Santa Rita - Sistema de Gestión Académica

Un sistema de escritorio ligero para la gestión de estudiantes, notas y asistencia[cite: 1]. Desarrollado en Python con una estética gráfica clásica estilo "Win2000"[cite: 1].

## 🚀 Características

* **Base de Datos Local:** Utiliza SQLite para crear automáticamente un archivo `registro_estudiantes.db`, manteniendo toda la información de forma local y privada[cite: 1].
* **Interfaz Organizada:** Interfaz gráfica construida con Tkinter, separada de forma estructurada en pestañas para "Datos Personales" y "Control Académico"[cite: 1].
* **Gestión de Calificaciones y Faltas:** Permite registrar inasistencias (a misa y a clase), notas de libro, puntos extra, exámenes y observaciones generales[cite: 1].
* **Búsqueda en Tiempo Real:** Panel de búsqueda integrado para filtrar y seleccionar estudiantes rápidamente[cite: 1].
* **Pantalla de Carga:** "Splash screen" de inicio asíncrono con soporte para cargar un logotipo personalizado (`logo.png`)[cite: 1].

## 🛠️ Tecnologías

* **Lenguaje:** Python 3.x[cite: 1]
* **Librerías:** `tkinter`, `sqlite3`, `os` (todas son nativas de Python, por lo que no se requiere instalar dependencias externas mediante `pip`)[cite: 1]

## ⚙️ Uso

Para ejecutar el programa, simplemente abre tu terminal en la carpeta del proyecto y ejecuta el archivo principal:
```bash
python santarita.py
