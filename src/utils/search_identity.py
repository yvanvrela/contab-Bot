import os
import requests
import logging
from dotenv import load_dotenv

from db.config.config_db import session
from db.repositories.contribuyentes_repository import ContribuyentesRepository
from utils.constants import TaxAuthority

load_dotenv()
logger = logging.getLogger(__name__)

URL_MEC_SEARCH = os.environ.get('URL_MEC_SEARCH', "https://www.mec.gov.py/cms_v4/denuncias/buscar_persona?documento=")

def search_identity_number(identity_number: str) -> dict | None:
    try:
        link = f"{URL_MEC_SEARCH}{identity_number.strip()}"
        # Se añade timeout de 5 segundos para evitar que el bot se congele si el MEC se cae
        response = requests.get(link, timeout=5).json()

        if response is not None and 'id_persona' in response:
            data = {
                'ci': response['id_persona'],
                'fullname': f"{response['nombre_persona']}, {response['apellido_persona']}",
            }
            return data
        else:
            return None
    except requests.exceptions.Timeout:
        logger.error(f"Timeout (5s) al intentar conectar con el MEC para CI: {identity_number}")
        return None
    except Exception as e:
        logger.error(f'Error searching MEC API: {e}')
        return None

def search_contribuyente(ruc: str) -> dict | None:
    """
    Retorna un diccionario con los datos consultando a SQLite.
    Puede discriminar guiones (-) y buscar por RUC o por CI.
    """
    ruc_reference = ruc.strip()
    repo = ContribuyentesRepository(session)

    if '-' in ruc_reference:
        # Search by RUC exactly
        contribuyente_db = repo.get_by_ruc(ruc_reference)
    else:
        # Search by CI exactly
        contribuyente_db = repo.get_by_ci(ruc_reference)

    if contribuyente_db:
        return {
            'ci': contribuyente_db.ci,
            'fullname': contribuyente_db.fullname,
            'ruc': contribuyente_db.ruc,
            'status': contribuyente_db.status
        }
    return None

def find_identity_data(identity_number: str) -> str:
    """
        Busca el numero de documento en SQLite (DNIT) y opcionalmente en el MEC si no lo encuentra.
    """
    # 1. Buscar en BD local de DNIT primero (Ultra rápido)
    contribuyente = search_contribuyente(identity_number)
    
    if contribuyente is not None:
        return f'*Es contribuyente*\nRUC: `{contribuyente["ruc"]}`\nNombre: `{contribuyente["fullname"]}`\nEstado: `{contribuyente["status"]}`'

    # 2. Si NO es contribuyente, recién ahí gastar tiempo consultando la web del MEC
    not_contribuyente = search_identity_number(identity_number)
    
    if not_contribuyente is not None:
        return f'*No es contribuyente*\nCI: `{not_contribuyente["ci"]}`\nNombre: `{not_contribuyente["fullname"]}`'

    return 'No encontré datos...'

