from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

#XPATHS
XPATH_SPRINGER_BTN_COOKIES = '/html/body/dialog/div/div/div[3]/button'
XPATH_SPRINGER_TITLE = '//*[@id="main"]/section/div/div/div[1]/h1'
XPATH_SPRINGER_CITA_TXT = '//p[contains(@class, "c-bibliographic-information__citation")]'
XPATH_SPRINGER_AUTORES_TXT = '//ul[@data-test="authors-list"]//a[@data-test="author-name"]'
XPATH_SPRINGER_BOOKTITLE_TXT = '//span[contains(@class, "app-article-masthead__journal-title")]'
XPATH_SPRINGER_YEAR_TXT = '//li[@class="c-bibliographic-information__list-item"]//time'
XPATH_SPRINGER_DOI_TXT = '//p[abbr[@title="Digital Object Identifier"]]/span[@class="c-bibliographic-information__value"]'
XPATH_SPRINGER_KEYWORDS_TXT = '//ul[@class="c-article-subject-list"]//li//a'
XPATH_SPRINGER_METRICS = '//ul[contains(@class, "app-article-metrics-bar")]/li'

#funciones:
def obtener_titulo_springer(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    # Intentar cerrar el diálogo de cookies si aparece
    try:
        btn_cookies = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_SPRINGER_BTN_COOKIES))
        )
        btn_cookies.click()
    except Exception:
        pass  # No apareció el botón, continuar
    titulo_elem = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_TITLE))
    )
    print("--->titulo_elem:",titulo_elem.text)
    return titulo_elem.text.strip()


def obtener_cita_springer(driver):
    #Para que quede parecido  "IEEE" se busca varios campos
    wait = WebDriverWait(driver, 5)
    cita_txt_elem = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_CITA_TXT))
    )
    cita_txt = cita_txt_elem.text.strip()
    
    autores_txt = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, XPATH_SPRINGER_AUTORES_TXT))
    )
    autores_txt = ", ".join([autor.text.strip() for autor in autores_txt])

    booktitle_txt = wait.until(
        EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_BOOKTITLE_TXT))
    )

    time_elem = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_YEAR_TXT))          )
    datetime_val = time_elem.get_attribute("datetime")
    datetime_val = datetime_val[:4]

    doi_elem = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SPRINGER_DOI_TXT)))
    doi_text = doi_elem.text.strip()
    if doi_text.startswith("https://doi.org/"):
        doi_text=doi_text.replace("https://doi.org/", "")
    
    keyword_elements = driver.find_elements(By.XPATH, XPATH_SPRINGER_KEYWORDS_TXT)
    keywords = [elem.text.strip() for elem in keyword_elements if elem.text.strip()]
    # print("-->cita_txt:",cita_txt)
    # print("-->autores_txt:",autores_txt)
    # print("-->booktitle_txt:",booktitle_txt.text)
    # print("-->2datetime_val:",datetime_val)
    # print("-->doi_text:",doi_text)
    # print("-->keywords:",keywords)

    return {
        "cita": cita_txt,
        "author": autores_txt,
        "booktitle": booktitle_txt.text,
        "year": datetime_val,
        "keywords": ", ".join(keywords),
        "doi": doi_text
    }


def parsear_bibtex(bibtex):
    resultado = {}
    matches = re.findall(r'(\w+)\s*=\s*[{"](.+?)[}"],?\s*$', bibtex, re.MULTILINE)
    for clave, valor in matches:
        resultado[clave.strip()] = valor.strip().rstrip("},")
    return resultado

def obtener_location_springer(driver):
        #En springer no aparece la locación en ningun lado.
        return "No Disponible"


def obtener_metricas_springer(driver):
    wait = WebDriverWait(driver, 10)
    cites_in = 0
    text_views = 0

    try:
        metricas = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, XPATH_SPRINGER_METRICS)
            )
        )
       
        for metrica in metricas:
            texto = metrica.text.strip()
            if "Accesses" in texto:
                text_views = int(texto.split()[0].replace(",", ""))
            elif "Citation" in texto or "Citations" in texto:
                cites_in = int(texto.split()[0].replace(",", ""))

    except Exception:
        pass  # si no hay métricas, se devuelven los ceros

    return cites_in, text_views
