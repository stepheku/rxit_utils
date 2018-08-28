import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import home_index
        request = testing.DummyRequest()
        info = home_index(request)
        self.assertEqual(info['project'], 'pyramid_app')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from rxit_utils import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Pharmacy Informatics Utilities' in res.body)

    def test_utils(self):
        res = self.testapp.get('/utilities', status=200)
        self.assertTrue(b'Report utilities' in res.body)
