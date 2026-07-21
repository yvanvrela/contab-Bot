import unittest
from db.config.config_db import session, ContribuyenteModel
from db.repositories.contribuyentes_repository import ContribuyentesRepository

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.repo = ContribuyentesRepository(session)
        # Aseguramos que haya un dato de prueba
        test_user = ContribuyenteModel(ci='9999999', ruc='9999999-1', dv='1', fullname='PRUEBA MAGIC SEARCH', status='ACTIVO')
        session.add(test_user)
        session.commit()

    def tearDown(self):
        # Limpiamos el dato de prueba
        session.query(ContribuyenteModel).filter(ContribuyenteModel.ci == '9999999').delete()
        session.commit()

    def test_search_by_name(self):
        results = self.repo.search_by_name('magic search', limit=5)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0].fullname, 'PRUEBA MAGIC SEARCH')

if __name__ == '__main__':
    unittest.main()
