from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.config.config_db import ContribuyenteModel
import logging

logger = logging.getLogger(__name__)

class ContribuyentesRepository:
    def __init__(self, session: Session):
        self.session = session

    def truncate_table(self) -> bool:
        """
        Elimina todos los registros de la tabla para preparar una nueva carga completa del DNIT.
        """
        try:
            self.session.query(ContribuyenteModel).delete()
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Error al vaciar la tabla de contribuyentes: {e}')
            return False

    def insert_bulk(self, contribuyentes_list: List[Dict]) -> bool:
        """
        Inserta una lista inmensa de diccionarios en la base de datos de manera optimizada.
        Espera una lista de diccionarios con las claves: ci, ruc, dv, fullname, status.
        """
        try:
            self.session.bulk_insert_mappings(ContribuyenteModel, contribuyentes_list)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f'Error en bulk insert de contribuyentes: {e}')
            return False

    def get_by_ci(self, ci: str) -> Optional[ContribuyenteModel]:
        try:
            return self.session.query(ContribuyenteModel).filter(ContribuyenteModel.ci == ci).first()
        except SQLAlchemyError as e:
            logger.error(f'Error al buscar por CI: {e}')
            return None

    def get_by_ruc(self, ruc: str) -> Optional[ContribuyenteModel]:
        try:
            return self.session.query(ContribuyenteModel).filter(ContribuyenteModel.ruc == ruc).first()
        except SQLAlchemyError as e:
            logger.error(f'Error al buscar por RUC: {e}')
            return None

    def search_by_name(self, name_query: str, limit: int = 5) -> List[ContribuyenteModel]:
        """
        Busca contribuyentes por nombre usando LIKE.
        """
        try:
            # SQLite LIKE is case-insensitive by default for ASCII characters.
            query = f"%{name_query.upper()}%"
            return self.session.query(ContribuyenteModel).filter(ContribuyenteModel.fullname.like(query)).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f'Error al buscar por Nombre: {e}')
            return []
