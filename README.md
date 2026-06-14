# Santa Rita - Sistema de Gestión para Catequesis

Un sistema de escritorio diseñado a la medida para facilitar la gestión de estudiantes, asistencia y calificaciones en grupos de catequesis. 

**🤖 Desarrollo mediante "Vibecoding"**
Este programa no fue escrito manualmente por un humano. Fue desarrollado íntegramente mediante inteligencia artificial (*vibecoding*), bajo supervisión humana, para ajustarse exactamente a las necesidades de los catequistas. Gracias a este método, el software se enfoca en ser **estrictamente funcional y práctico**. No posee una estética fija ni busca ser un programa visualmente moderno; su único objetivo es cumplir con el trabajo de forma rápida y sin complicaciones.

## 🚀 Características

* **Base de Datos Local:** Utiliza SQLite para crear automáticamente un archivo `registro_estudiantes.db`, manteniendo toda la información de forma local y privada en el equipo.
* **Control Específico para Catequesis:** Permite registrar métricas clave como inasistencias (a misa y a clase), notas de libro, puntos extra, exámenes y observaciones generales.
* **Interfaz Práctica:** Interfaz gráfica construida con Tkinter bajo un estilo visual clásico ("Win2000")[cite: 1], separada en pestañas para "Datos Personales" y "Control Académico".
* **Búsqueda en Tiempo Real:** Panel integrado para filtrar y seleccionar estudiantes rápidamente desde la lista.
* **Pantalla de Carga:** "Splash screen" de inicio asíncrono preparado para mostrar un logotipo institucional (`logo.png`).

## 🛠️ Tecnologías

* **Lenguaje:** Python 3.x.
* **Librerías:** `tkinter`, `sqlite3`, `os` (todas son nativas de Python, por lo que no se requiere instalar dependencias externas mediante `pip`).

## ⚙️ Uso

Para ejecutar el programa, simplemente abre tu terminal en la carpeta del proyecto y ejecuta el archivo principal:

```bash
python santarita.py
