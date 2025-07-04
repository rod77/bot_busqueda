from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
from pathlib import Path
import shutil

# 📄 CONFIG
ORIGINAL_XLSX = Path("ExcelModelo/ExcelModelo.xlsx")
COPIA_XLSX = Path("Resumen.xlsx")
URLS = [
    "https://ieeexplore.ieee.org/document/10937826",
    'https://ieeexplore.ieee.org/document/4053283',
    "https://ieeexplore.ieee.org/document/10993799",
    "https://ieeexplore.ieee.org/document/8397647",
    'https://ieeexplore.ieee.org/document/6493605',
    'https://ieeexplore.ieee.org/document/10270721',
    'https://ieeexplore.ieee.org/document/10121659',
    'https://ieeexplore.ieee.org/document/9006200',
    'https://ieeexplore.ieee.org/document/10158172',
    'https://ieeexplore.ieee.org/document/10423308'
]

#Funciones de IEEE
from FN_IEEE import (
    obtener_titulo_ieee,
    obtener_cita_ieee,
    obtener_location_ieee,
    obtener_metricas_ieee
)

#Funciones Utiles
def copiar_excel(origen: Path, destino: Path):
    shutil.copy(origen, destino)
    print(f"Copiando Excel...")

def inicializar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def obtener_urls_existentes(ws, fila=2, desde_columna=4):
    urls = set()
    col = desde_columna
    while ws.cell(row=fila, column=col).value:
        urls.add(ws.cell(row=fila, column=col).value.strip())
        col += 1
    return urls

def encontrar_columna_libre(ws, fila=1, desde_columna=4):
    col = desde_columna
    while ws.cell(row=fila, column=col).value:
        col += 1
    return col

def escribir_articulo_en_excel(ws, col, articulo):
    ws.cell(row=1, column=col, value=articulo["id"])
    ws.cell(row=2, column=col, value=articulo["link"])
    ws.cell(row=3, column=col, value=articulo["title"])
    ws.cell(row=4, column=col, value=articulo["author"])
    ws.cell(row=5, column=col, value=articulo["year"])
    ws.cell(row=7, column=col, value=articulo["fuente"])
    ws.cell(row=8, column=col, value=articulo["booktitle"])
    ws.cell(row=9, column=col, value=articulo["ubicacion"])
    ws.cell(row=10, column=col, value=articulo["cites_in"])
    ws.cell(row=11, column=col, value=articulo["keywords"])
    ws.cell(row=12, column=col, value=articulo["cita"])
    ws.cell(row=13, column=col, value=articulo["doi"])
    ws.cell(row=14, column=col, value=articulo["text_views"])

# Main:
if __name__ == "__main__":
    # abrir/crear Excel
    if COPIA_XLSX.exists():
        wb = load_workbook(COPIA_XLSX)
        print("Excel existente.")
    else:
        copiar_excel(ORIGINAL_XLSX, COPIA_XLSX)
        wb = load_workbook(COPIA_XLSX)
        print("Creando Excel")
    ws = wb["Resumen"]

    urls_existentes = obtener_urls_existentes(ws)
    driver = inicializar_driver()

    for url in URLS:
        if url in urls_existentes:
            print(f"-URL Ya Incorporada: {url}")
            continue

        print(f"Procesando: {url}")

        titulo = obtener_titulo_ieee(driver, url)
        ubicacion = obtener_location_ieee(driver)
        cites_in, text_views = obtener_metricas_ieee(driver)
        datos_cita = obtener_cita_ieee(driver)

        col_libre = encontrar_columna_libre(ws)
        articulo = {
            "id": col_libre - 3,
            "link": url,
            "title": titulo,
            "cita": datos_cita["cita"],
            "author": datos_cita["author"],
            "booktitle": datos_cita["booktitle"],
            "year": int(datos_cita["year"]) if str(datos_cita["year"]).isdigit() else 0,
            "keywords": datos_cita["keywords"],
            "doi": datos_cita["doi"],
            "fuente": "IEEE",
            "ubicacion": ubicacion,
            "cites_in": cites_in,
            "text_views": text_views
        }

        escribir_articulo_en_excel(ws, col_libre, articulo)
        wb.save(COPIA_XLSX)

    driver.quit()
    print("Proceso Finalizado.")
