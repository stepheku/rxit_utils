import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()


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

    def test_utils_pwrpln_color(self):
        res = self.testapp.get('/utilities/powerplan_colors', status=200)
        self.assertTrue(b'pathway_component_id' in res.body)

    def test_utils_pwrpln_color_test(self):
        """Testing different inputs for updating powerplan colors
        utility
        1. """
        res = self.testapp.post('/utilities/powerplan_colors_submit',
                                {
                                    'pathway_comp_ids': '1234\n2345\n3456',
                                    'color_value': 'd2d2a6'
                                })
        self.assertTrue(b'00d2d2a6' in res.body)
        self.assertTrue(b'BackColor&gt;00d2d2a6&lt;/BackColor' in res.body)
