import unittest
from db.config.config_db import session, ContribuyenteModel
from db.repositories.contribuyentes_repository import ContribuyentesRepository

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.repo = ContribuyentesRepository(session)
        # Aseguramos que haya un dato de prueba
        test_user1 = ContribuyenteModel(ci='9999999', ruc='9999999-1', dv='1', fullname='PRUEBA MAGIC SEARCH', status='ACTIVO')
        test_user2 = ContribuyenteModel(ci='8888', ruc='8888-1', dv='1', fullname='GONZALEZ NUÑEZ, MARÍA JOSE', status='ACTIVO')
        session.add(test_user1)
        session.add(test_user2)
        session.commit()

    def tearDown(self):
        # Limpiamos el dato de prueba
        session.query(ContribuyenteModel).filter(ContribuyenteModel.ci.in_(['9999999', '8888'])).delete()
        session.commit()

    def test_search_by_name_original(self):
        results = self.repo.search_by_name('magic search', limit=5)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0].fullname, 'PRUEBA MAGIC SEARCH')

    def test_search_insensitive_to_accents_and_order(self):
        # Búsqueda 1: "MARIA GONZALEZ"
        results1 = self.repo.search_by_name('MARIA GONZALEZ', limit=10000)
        self.assertTrue(any(r.ci == '8888' for r in results1))

        # Búsqueda 2: "jose núñez"
        results2 = self.repo.search_by_name('jose núñez', limit=10000)
        self.assertTrue(any(r.ci == '8888' for r in results2))

        # Búsqueda 3: "núñez maría"
        results3 = self.repo.search_by_name('núñez maría', limit=10000)
        self.assertTrue(any(r.ci == '8888' for r in results3))

if __name__ == '__main__':
    unittest.main()
