from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

#XPATHS
XPATH_SPRINGER_TITLE = '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span'
XPATH_SPRINGER_CITA_BTN = '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/div/div[2]/xpl-cite-this-modal/div/button'
XPATH_SPRINGER_CITA_TXT = '/html/body/ngb-modal-window/div/div/div/div[3]/div[2]'
XPATH_SPRINGER_CITA_BIBTEX_BTN = '/html/body/ngb-modal-window/div/div/div/div[2]/nav/div[2]/a'
XPATH_SPRINGER_CITA_BIBTEX_TXT = '/html/body/ngb-modal-window/div/div/div/div[3]/pre'
XPATH_SPRINGER_MODAL_CLOSE = '/html/body/ngb-modal-window/div/div/div/div[3]/button/i'
XPATH_SPRINGER_LOCATION = '//div[contains(@class, "doc-abstract-conferenceLoc")]'

#funciones:
def obtener_titulo_springer(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    titulo_elem = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_TITLE))
    )
    return titulo_elem.text.strip()


def obtener_cita_springer(driver):
    wait = WebDriverWait(driver, 15)

    btn_citar = wait.until(
        EC.element_to_be_clickable((By.XPATH, XPATH_SPRINGER_CITA_BTN))
    )
    
    btn_citar.click()

    cita_texto = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_CITA_TXT))
    )
    cita = cita_texto.text.strip()

    btn_bibtex = wait.until(
        EC.element_to_be_clickable((By.XPATH, XPATH_SPRINGER_CITA_BIBTEX_BTN))
    )
    btn_bibtex.click()

    bibtex_texto = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_CITA_BIBTEX_TXT))
    )
    bibtex = bibtex_texto.text.strip()

    driver.find_element(By.XPATH, XPATH_SPRINGER_MODAL_CLOSE).click()

    parsed = parsear_bibtex(bibtex)

    return {
        "cita": cita,
        "author": parsed.get("author", ""),
        "booktitle": parsed.get("booktitle", ""),
        "year": int(parsed.get("year", "0")) if parsed.get("year", "0").isdigit() else 0,
        "keywords": parsed.get("keywords", ""),
        "doi": parsed.get("doi", "")
    }


def parsear_bibtex(bibtex):
    resultado = {}
    matches = re.findall(r'(\w+)\s*=\s*[{"](.+?)[}"],?\s*$', bibtex, re.MULTILINE)
    for clave, valor in matches:
        resultado[clave.strip()] = valor.strip().rstrip("},")
    return resultado

def obtener_location_springer(driver):
    wait = WebDriverWait(driver, 15)

    try:
        loc_elemento = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, XPATH_IEEE_LOCATION)
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


def obtener_metricas_springer(driver):
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
