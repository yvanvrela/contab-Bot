from services.ruc_downloader import URL, PATH, find_zip_url, scan_files, download_zips, unzipping_files
from unittest import TestCase
import unittest
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MainTest(TestCase):

    def test_find_zip_url(self):
        list_zip_url = find_zip_url(url=URL)

        self.assertEqual(len(list_zip_url), 10)
        logger.info('Test find rucs url complete...')

    def test_download_zip_rucs(self):
        download_zips()
        list_files = scan_files('.zip')

        self.assertEqual(len(list_files), 10)
        logger.info('Test download ruc files complete...')

    def test_unziping_rucs(self):
        unzipping_files()
        
        # Como ahora unzipping_files inserta en BD y borra los TXT, debe haber 0 TXT
        list_files = scan_files('.txt')
        self.assertEqual(len(list_files), 0)
        
        # Validar inserción en base de datos
        from db.config.config_db import session, ContribuyenteModel
        count = session.query(ContribuyenteModel).count()
        self.assertGreater(count, 0)
        logger.info(f'Test unzipping rucs file complete. {count} contribuyentes en BD.')

if __name__ == '__main__':
    unittest.main()
