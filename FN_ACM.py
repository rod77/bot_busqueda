from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time

#XPATHS
XPATH_ACM_TITLE = '//*[@id="skip-to-main-content"]/main/article/header/div/h1'
XPATH_ACM_CITA_BTN = '//*[@id="skip-to-main-content"]/main/article/header/div/div[7]/div[2]/div[3]/button'
#XPATH_ACM_CITA_TXT = '/html/body/ngb-modal-window/div/div/div/div[3]/div[2]'
#XPATH_ACM_CITA_BIBTEX_BTN = '/html/body/ngb-modal-window/div/div/div/div[2]/nav/div[2]/a'
#XPATH_ACM_CITA_BIBTEX_TXT = '/html/body/ngb-modal-window/div/div/div/div[3]/pre'
#XPATH_ACM_MODAL_CLOSE = '/html/body/ngb-modal-window/div/div/div/div[3]/button/i'
XPATH_ACM_LOCATION = '//div[contains(@class, "doc-abstract-conferenceLoc")]'

#funciones:
def obtener_titulo_acm(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 5)

# Intentar aceptar cookies si el botón aparece
    try:
        boton_cookies = wait.until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        boton_cookies.click()
    except (TimeoutException, NoSuchElementException):
        print("")


    titulo_elem = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_ACM_TITLE))
    )
    print("-->Title ACM:",titulo_elem.text)
    return titulo_elem.text.strip()


def obtener_cita_acm(driver):
    wait = WebDriverWait(driver, 15)

    # Hacer click en el boton de export citation
    time.sleep(5)
    boton_cita = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_ACM_CITA_BTN)))
    boton_cita.click()
    time.sleep(5)
    # Esperar a que cargue el modal con la cita en formato bibtex
    cita_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "csl-right-inline")))
    cita_texto = cita_elem.text.strip()

    author_raw = extraer_valor_bibtex(cita_texto, "author")
    author = author_raw.replace(",", "")

    print("cita",cita_texto)
    print("author",author)
    print("booktitle",extraer_valor_bibtex(cita_texto, "publisher"))
    print("year",extraer_valor_bibtex(cita_texto, "year"))
    print("keywords",extraer_valor_bibtex(cita_texto, "keywords"))
    print("doi",extraer_valor_bibtex(cita_texto, "doi"))

    return {
        "cita": cita_texto,
        "author": author,
        "booktitle": extraer_valor_bibtex(cita_texto, "publisher"),
        "year": extraer_valor_bibtex(cita_texto, "year"),
        "keywords": extraer_valor_bibtex(cita_texto, "keywords"),
        "doi": extraer_valor_bibtex(cita_texto, "doi"),
    }


def extraer_valor_bibtex(texto, campo):
    patron = rf'{campo}\s*=\s*\{{(.*?)\}}'
    resultado = re.search(patron, texto, re.DOTALL)
    return resultado.group(1).strip() if resultado else ""

def obtener_location_acm(driver):
    wait = WebDriverWait(driver, 5)

    try:
        loc_elemento = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, XPATH_ACM_LOCATION)
            )
        )
        texto = loc_elemento.text.strip()
        # quito prefijo
        if texto.startswith("Conference Location:"):
            texto = texto.replace("Conference Location:", "", 1).strip()

        # Me quedo con el pais
        if "," in texto:
            ubicacion = texto.split(",")[-1].strip()
        else:
            ubicacion = texto

        return ubicacion

    except Exception as e:
        return "No Disponible"


def obtener_metricas_acm(driver):
    wait = WebDriverWait(driver, 10)

    cites_in = 0
    text_views = 0

    try:
        botones = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[contains(@class, 'document-banner-metric')]")
            )
        )

        for btn in botones:
            texto = btn.text.strip()

            try:
                numero_txt = btn.find_element(
                    By.XPATH, ".//div[contains(@class,'document-banner-metric-count')]"
                ).text.strip()
                numero = int(numero_txt.replace(",", ""))
            except:
                numero = 0

            if "Cites in" in texto:
                cites_in = numero
            elif "Text Views" in texto:
                text_views = numero

    except Exception as e:
        #print(f"⚠️ No se encontraron métricas: {e}")
        pass

    return cites_in, text_views
