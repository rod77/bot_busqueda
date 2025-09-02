# 📚 Automatización y Análisis de Artículos Académicos

Este proyecto permite automatizar la extracción de información clave de artículos provenientes de bibliotecas digitales como **IEEE Xplore**, **SpringerLink** y **ACM Digital Library**.  
Fue desarrollado como trabajo práctico final para el seminario *"Herramientas para el desarrollo de tesis"* de la **Maestría en Ingeniería de Sistemas de Información – UTN**.

## 🎯 Objetivo

Herramienta simple y eficiente para reducir el tiempo necesario para recopilar, organizar y analizar artículos académicos.  
El resultado es un archivo Excel (Resumen.xlsx) con todos los datos obtenidos, gráficos y métricas que ayudae a tomar decisiones para nuestra tesis.

---

## ⚙️ ¿Qué hace la herramienta?

- Extrae automáticamente desde un Excel con URLs de las diferentes bibliotecas, la siguiente información:
  - Título
  - Autores
  - Año
  - Fuente (revista o conferencia)
  - Tipo de investigación
  - País
  - DOI
  - Citas
  - Vistas
  - Keywords
- Genera un archivo `Resumen.xlsx` con:
  - 📄 Hoja **Resumen**: datos organizados por artículo
  - 📊 Hoja **Gráficos**: visualizaciones por año, país, fuente, keywords
  - 📈 Hoja **Métricas**: top artículos citados/vistos, promedios y más

---

## 💻 Tecnologías utilizadas

- Todo desarrollado en: `Python`
- `Selenium` – para navegación automatizada y la extracción de datos.
- `openpyxl` – para manipulación de archivos Excel.

---

## 📦 Instalación desde código fuente
```bash
git clone https://github.com/rod77/bot_busqueda.git
cd bot_busqueda
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```
---

## ✅ Ventajas en el uso de la herramienta:

- Ahorra tiempo
- Reduce errores manuales
- Facilita la organización de artículos
- Ayuda a detectar artículos irrelevantes
- Brinda métricas objetivas de calidad

---

## 🧠 Créditos
Desarrollado por Ing. Rodrigo Maestre – **UTN**.  
Trabajo Final – Seminario: Herramientas para el desarrollo de tesis.  
Maestría en Ingeniería de Sistemas de Información.
