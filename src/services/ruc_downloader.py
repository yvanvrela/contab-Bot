import os
from bs4 import BeautifulSoup
import re
import requests
import zipfile
import logging

from utils.export_files import delete_file
from utils.constants import TaxAuthority
from db.config.config_db import session
from db.repositories.contribuyentes_repository import ContribuyentesRepository

logger = logging.getLogger(__name__)

PATH = os.path.join(os.path.dirname(__file__), '..', 'archives', 'rucs')
SET_URL = 'https://www.dnit.gov.py'
URL = 'https://www.dnit.gov.py/web/portal-institucional/listado-de-ruc-con-sus-equivalencias'

# Para soporte de SSL (Ignorar si urllib3 v2+ no lo soporta)
try:
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

def ensure_dir():
    if not os.path.exists(PATH):
        os.makedirs(PATH, exist_ok=True)

def download_zips(progress_callback=None) -> None:
    ensure_dir()
    try:
        if progress_callback:
            progress_callback(f"Conectando con la {TaxAuthority.NAME.value}... 🌐")
            
        url_list = find_zip_url(URL)
        total = len(url_list)
        
        for index, url in enumerate(url_list, 1):
            page = requests.get(url)
            patron = 'ruc.+\.zip'
            ruc_filename = re.findall(patron, url)[0]
            filename = os.path.join(PATH, ruc_filename)

            with open(filename, 'wb') as output_file:
                output_file.write(page.content)
            
            logger.info(f"Descargado: {ruc_filename}")
            if progress_callback:
                progress_callback(f"Descargando archivo ZIP {index} de {total}... 📦")
                
    except Exception as e:
        logger.error(f"Error descargando ZIPs: {e}")
        if progress_callback:
            progress_callback(f"❌ Error al descargar: {e}")

def find_zip_url(url: str) -> list:
    page_ruc = requests.get(url)
    soup = BeautifulSoup(page_ruc.content, 'html.parser')
    links_ruc_page = soup.find_all('div', class_='item__links')

    list_url_zip = [f'{SET_URL}{page.find("a").get("href")}' for page in links_ruc_page]
    return list_url_zip

def read_file(path: str) -> list:
    contribuyentes = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if not line.strip():
                continue

            # 10000|APELLIDO, NOMBRES|DV|XXXXXX|ESTADO|
            data = line.split('|')
            if len(data) < 5:
                continue
                
            fullname = data[1]
            contribuyentes.append(
                {
                    'ci': data[0],
                    'dv': data[2],
                    'fullname': fullname,
                    'ruc': f'{data[0]}-{data[2]}',
                    'status': data[4],
                }
            )
    return contribuyentes

def scan_files(file_extension='.txt', end_ruc=None) -> list | str:
    ensure_dir()
    path_rucs = PATH

    if end_ruc is not None:
        if end_ruc == '*':
            with os.scandir(path_rucs) as ficheros:
                files = [os.path.join(path_rucs, fichero.name) for fichero in ficheros if fichero.is_file() and fichero.name.endswith(file_extension)]
            return files
        else:
            filename = os.path.join(path_rucs, f'ruc{end_ruc}.txt')
            return filename
    else:
        with os.scandir(path_rucs) as ficheros:
            files = [os.path.join(path_rucs, fichero.name) for fichero in ficheros if fichero.is_file() and fichero.name.endswith(file_extension)]
        return files

def unzipping_files(progress_callback=None) -> None:
    paths_zip = scan_files('.zip')
    total_zips = len(paths_zip)
    
    if progress_callback:
        progress_callback(f"Descomprimiendo {total_zips} archivos ZIP... 🗜️")
        
    # 1. Unzip all
    for path in paths_zip:
        try:
            with zipfile.ZipFile(path, 'r') as zip_reference:
                zip_reference.extractall(PATH)
            delete_file(path)
            logger.info(f"Descomprimido y borrado ZIP: {path}")
        except Exception as e:
            logger.error(f"Error extrayendo {path}: {e}")

    # 2. Insert into DB
    if progress_callback:
        progress_callback("Vaciando tabla vieja de contribuyentes... 🧹")
        
    repo = ContribuyentesRepository(session)
    logger.info("Vaciando tabla vieja de contribuyentes...")
    repo.truncate_table()

    paths_txt = scan_files('.txt')
    total_txt = len(paths_txt)
    
    for index, path in enumerate(paths_txt, 1):
        if progress_callback:
            progress_callback(f"Inyectando en BD archivo {index} de {total_txt}... 💾\n*(Esto tomará un minuto)*")
            
        logger.info(f"Procesando {path} para inserción en BD...")
        try:
            data = read_file(path)
            repo.insert_bulk(data)
            delete_file(path)
            logger.info(f"Insertado en BD y borrado TXT: {path}")
        except Exception as e:
            logger.error(f"Error procesando TXT {path}: {e}")
            if progress_callback:
                progress_callback(f"❌ Error al inyectar datos: {e}")
