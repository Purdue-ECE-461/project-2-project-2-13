import json

import db
from openapi_server.models.package import Package
from openapi_server.models.package_data import PackageData
from openapi_server.models.package_metadata import PackageMetadata
from query_handler.operations.create_operation import CreateOperation
from query_handler.queries.package_query import PackageQuery
from query_handler.test import BaseTestCase


class TestPackage(BaseTestCase):
    def test_package_create(self):
        expected = Package(PackageMetadata('example name', '1.2.3', '0'), PackageData('example content', 'example URL', 'example JS_Program'))
        query = PackageQuery(CreateOperation(), expected)
        actual = query.execute()
        assert actual == expected
    def test_package_read(self):
        pass

    def test_package_update(self):
        pass

    def test_package_delete(self):
        pass
