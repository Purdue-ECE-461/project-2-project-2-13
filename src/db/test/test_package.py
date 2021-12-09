import db
from db.test import BaseTestCase
from openapi_server.models.package import Package, PackageMetadata, PackageData

class TestDbPackage(BaseTestCase):
    def test_get(self):
        expected = {'metadata': {'name': 'test', 'version': '1.2.3', 'id': id}, 'data': {'content': 'Content', 'url': 'URL', 'js_program': 'JS_Program'}}
        db.DB['package'][id] = expected

        actual = db.get('package', id)

        assert actual == expected

    def test_set(self):
        expected = {'metadata': {'name': 'test', 'version': '1.2.3', 'id': id}, 'data': {'content': 'Content', 'url': 'URL', 'js_program': 'JS_Program'}}
        
        db.set('package', id, expected)

        actual = db.DB['package'][id]
        
        assert actual == expected
        