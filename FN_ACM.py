from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time

#XPATHS
XPATH_ACM_TITLE = '//*[@id="skip-to-main-content"]/main/article/header/div/h1'
XPATH_ACM_CITA_BTN = '//*[@id="skip-to-main-content"]/main/article/header/div/div[7]/div[2]/div[3]/button'
XPATH_ACM_AUTORES = '//span[@property="author" and @typeof="Person"]'
XPATH_ACM_ANIO = '//*[@id="skip-to-main-content"]/main/article/header/div/div[5]//span[@class="core-date-published"]'
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


def obtener_autores_acm(driver):
    wait = WebDriverWait(driver, 10)
    autores_final = []

    try:
        autores_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, XPATH_ACM_AUTORES))
        )
        for autor in autores_elements:
            try:
                nombre = autor.find_element(By.XPATH, './/span[@property="givenName"]').text.strip()
                apellido = autor.find_element(By.XPATH, './/span[@property="familyName"]').text.strip()
                autores_final.append(f"{nombre} {apellido}")
            except Exception:
                continue  # saltea si no encuentra alguno

    except Exception as e:
        print("No se encontraron autores:", e)

    return ", ".join(autores_final)

def obtener_anio_acm(driver):
    try:
        wait = WebDriverWait(driver, 10)
        
        fecha_elem = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_ACM_ANIO)))
        fecha_texto = fecha_elem.text.strip()

        print("--> Fecha publicada:", fecha_texto)  # Ej: "08 November 2020"

        # Extraer el último token como año
        anio = int(fecha_texto.strip().split()[-1])
        return anio

    except Exception as e:
        print(f"[ERROR] No se pudo obtener el año de publicación: {e}")
        return 0

def obtener_booktitle_acm(driver):
    wait = WebDriverWait(driver, 10)

    try:
        # Paso 1: Hacer clic en "Authors Info & Claims"
        boton_authors_info = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="skip-to-main-content"]/main/article/header/div/div[3]/a'))
        )
        boton_authors_info.click()

        # Paso 2: Hacer clic en "Information"
        boton_information = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information-label"]'))
        )
        boton_information.click()

        # Paso 3: Buscar sección "Conference"
        secciones = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tab-information"]/section'))
        )

        for seccion in secciones:
            try:
                h4 = seccion.find_element(By.TAG_NAME, "h4")
                if h4.text.strip().lower() == "conference":
                    booktitle_tag = seccion.find_element(By.XPATH, './/div[contains(@class,"core-conference-right")]/a')
                    texto_conferencia = booktitle_tag.text.strip()
                    print("--> Booktitle (conferencia):", texto_conferencia)
                    return texto_conferencia
            except Exception:
                continue

        print("[WARN] No se encontró sección de conferencia.")
        return ""

    except Exception as e:
        print(f"[ERROR] No se pudo obtener el booktitle: {e}")
        return ""

def obtener_keyword_acm(driver):
    wait = WebDriverWait(driver, 10)
    try:
        try:
            # Paso 1: Hacer clic en "Authors Info & Claims"
            boton_key_info = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="skip-to-main-content"]/main/article/header/div/div[3]/a'))
            )
            boton_key_info.click()

            # Paso 2: Hacer clic en "Information"
            boton_information = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information-label"]'))
            )
            boton_information.click()
        except:
            pass
            # Paso 3: Buscar sección "Conference"
            secciones = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tab-information"]/section'))
            )

            for seccion in secciones:
                try:
                    h4 = seccion.find_element(By.TAG_NAME, "h4")
                    if h4.text.strip().lower() == "author tags":
                        key_tags = seccion.find_elements(By.XPATH, './/ol/li/a')
                        keywords = [k.text.strip() for k in key_tags if k.text.strip()]
                        texto_keywords = ", ".join(keywords)
                        print("--> KeyWords ", texto_keywords)
                        return texto_keywords
                except Exception:
                    continue

            print("[WARN] No se encontró sección de conferencia.")
            return ""
    except:
        return "No Disponible"

def obtener_doi_acm(driver):
    wait = WebDriverWait(driver, 10)
    try:
        doi_link = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="skip-to-main-content"]/main/article/header/div/div[4]/div[3]/a')
            )
        )
        href = doi_link.get_attribute("href")
        doi = href.replace("https://doi.org/", "").strip()
        print("--> DOI:", doi)
        return doi
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el DOI: {e}")
        return ""


def obtener_cita_acm(driver):

    author = obtener_autores_acm(driver)
    anio = obtener_anio_acm(driver)
    doi = obtener_doi_acm(driver)
    booktitle = obtener_booktitle_acm(driver)
    key = obtener_keyword_acm(driver)
    return {
        "cita": "",
        "author": author,
        "booktitle":booktitle,
        "year": anio,
        "keywords": key,
        "doi": doi ,
    }


def extraer_valor_bibtex(texto, campo):
    patron = rf'{campo}\s*=\s*\{{(.*?)\}}'
    resultado = re.search(patron, texto, re.DOTALL)
    return resultado.group(1).strip() if resultado else ""

def obtener_location_acm(driver):
    wait = WebDriverWait(driver, 10)

    try:
        # # Paso 1: Hacer clic en "Authors Info & Claims"
        try:
            boton_authors_info = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="skip-to-main-content"]/main/article/header/div/div[3]/a'))
            )
            boton_authors_info.click()

            # Paso 2: Hacer clic en "Information"
            boton_information = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information-label"]'))
            )
            boton_information.click()
        except:
            pass

        # Paso 3: Buscar sección "Conference"
        secciones = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tab-information"]/section'))
        )
        for seccion in secciones:
            try:
                h4 = seccion.find_element(By.TAG_NAME, "h4")
                if h4.text.strip().lower() == "conference":
                    country_tag = seccion.find_element(By.XPATH, './/div[contains(@class,"core-conference-map")]')
                    texto_country = country_tag.text.strip()
                    if "," in texto_country:
                        country = texto_country.split(",")[-1].strip()
                    else:
                        country = texto_country
                    print("--> Country:", country)
                    return country
            except Exception:
                continue

        #print("[WARN] No se encontró sección de conferencia.")
        return "No Disponible"

    except Exception as e:
        #print(f"[ERROR] No se pudo obtener el booktitle: {e}")
        return "No Disponible"


def obtener_metricas_acm(driver):
    wait = WebDriverWait(driver, 10)
    try:
        # Esperar al botón de métricas
        metrics_btn = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".info-panel__metrics .metrics-toggle")
        ))

        # Buscar los spans dentro del botón (citations y downloads)
        spans = metrics_btn.find_elements(By.TAG_NAME, "span")

        cites_in = 0
        text_views = 0

        for i, span in enumerate(spans):
            try:
                text = span.text.strip()
                if text.isdigit():
                    num = int(text)
                    # Heurística: primer número = citas, segundo número = vistas
                    if cites_in == 0:
                        cites_in = num
                    elif text_views == 0:
                        text_views = num
            except:
                continue

        print("--> Citas (citations):", cites_in)
        print("--> Descargas (downloads):", text_views)

        return cites_in, text_views

    except Exception as e:
        print(f"[ERROR] No se pudieron obtener las métricas: {e}")
        return 0, 0
