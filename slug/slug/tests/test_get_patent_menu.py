import unittest
import os
import json

from slug.patent_menu_getter import PatentMenuGetter

current_dir = os.path.dirname(__file__)





class PatentMenuGetTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_parse_request_parameter(self):
        parameter = self.get_menu_request_parameter_json()
        self.assertEqual(0,parameter["query"]["from"])
        self.assertEqual(20,parameter["query"]["size"])

    def get_menu_request_parameter_json(self):
        with open(os.path.join(current_dir, "resources", "menu_get_parameter.json"), 'r', encoding="utf8") as f:
            request_parameter = "".join(f.readlines())
            parameter = json.loads(request_parameter)
        return parameter

    def test_get_base_url(self):
        getter = PatentMenuGetter()
        self.assertEqual("https://worldwide.espacenet.com/3.2/rest-services/search",getter.base_url)


    def test_do_request(self):
        getter = PatentMenuGetter()
        data = self.get_menu_request_parameter_json()
        getter.request("A61K38%2F00",data)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(PatentMenuGetTest('test_parse_request_parameter'))
    runner = unittest.TextTestRunner()
    runner.run(suite)

