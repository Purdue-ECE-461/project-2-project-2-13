# coding: utf-8

from __future__ import absolute_import

import unittest

import db
from flask import json
from openapi_server.models.error import Error
from openapi_server.models.package import Package
from openapi_server.models.package_history_entry import PackageHistoryEntry
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.package_query import PackageQuery
from openapi_server.models.package_rating import PackageRating
from openapi_server.test import BaseTestCase
from query_handler.operations.create_operation import CreateOperation
from query_handler.operations.read_operation import ReadOperation
from query_handler.queries.package_query import PackageQuery as PackageQueryDb
from six import BytesIO


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_package_by_name_delete(self):
        """Test case for package_by_name_delete

        Delete all versions of this package.
        """
        # Insert the package
        package = Package.from_dict(
            {
                "metadata" : {
                    "Version" : "1.2.3",
                    "ID" : "id_example",
                    "Name" : "name_example"
                },
                    "data" : {
                        "Content" : "content_example",
                        "JSProgram" : "jsprogram_example",
                        "URL" : "url_example"
                }
            }
        )
        PackageQueryDb(CreateOperation(), package).execute()

        response = self.client.open(
            '/package/byName/{name}'.format(name=package.metadata.name),
            method='DELETE',
            headers={})

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_package_by_name_get(self):
        """Test case for package_by_name_get

        
        """
        # Insert the package
        package = Package.from_dict(
            {
                "metadata" : {
                    "Version" : "1.2.3",
                    "ID" : "id_example",
                    "Name" : "name_example"
                },
                    "data" : {
                        "Content" : "content_example",
                        "JSProgram" : "jsprogram_example",
                        "URL" : "url_example"
                }
            }
        )
        PackageQueryDb(CreateOperation(), package).execute()

        response = self.client.open(
            '/package/byName/{name}'.format(name='name_example'),
            method='GET',
            headers={})

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assert json.loads(response.data)[0]['PackageMetadata'] == package.metadata.to_dict()

    def test_package_create(self):
        """Test case for package_create

        
        """
        package = {
            "metadata" : {
                "Version" : "1.2.3",
                "ID" : "id_example",
                "Name" : "name_example"
            },
            "data" : {
                "Content" : "content_example",
                "JSProgram" : "jsprogram_example",
                "URL" : "url_example"
            }
        }
        response = self.client.open(
            '/package',
            method='POST',
            headers={},
            data=json.dumps(package),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # get package from DB
        data = PackageQueryDb(ReadOperation(), Package.from_dict(package)).execute().to_dict()
        assert(package == data)

    def test_package_delete(self):
        """Test case for package_delete

        Delete this version of the package.
        """
        # insert package into DB
        package = {
            "metadata" : {
                "Version" : "1.2.3",
                "ID" : "ID",
                "Name" : "Name"
            },
            "data" : {
                "Content" : "Content",
                "JSProgram" : "JSProgram",
                "URL" : "URL"
            }
        }
        PackageQueryDb(CreateOperation(), Package.from_dict(package)).execute()
        # delete the package
        response = self.client.open(
            '/package/{id}'.format(id=package['metadata']['ID']),
            method='DELETE',
            headers={})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # try to get package from DB
        data = PackageQueryDb(ReadOperation(), Package.from_dict(package)).execute()
        assert(data == None)


    def test_package_rate(self):
        """Test case for package_rate

        
        """
        headers = { 
        }
        response = self.client.open(
            '/package/{id}/rate'.format(id='id_example'),
            method='GET',
            headers=headers)
        # self.assert200(response,
        #                'Response body is : ' + response.data.decode('utf-8'))

    def test_package_retrieve(self):
        """Test case for package_retrieve

        
        """
        # Insert the package
        package = Package.from_dict(
            {
                "metadata" : {
                    "Version" : "1.2.3",
                    "ID" : "ID",
                    "Name" : "Name"
                },
                "data" : {
                    "Content" : "Content",
                    "JSProgram" : "JSProgram",
                    "URL" : "URL"
                }
            }
        )
        PackageQueryDb(CreateOperation(), package).execute()

        response = self.client.open(
            '/package/{id}'.format(id=package.metadata.id),
            method='GET',
            headers={})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        

    def test_package_update(self):
        """Test case for package_update

        Update this version of the package.
        """
        # insert the package
        package = {
            "metadata" : {
                "Version" : "1.2.3",
                "ID" : "ID",
                "Name" : "Name"
            },
            "data" : {
                "Content" : "Content",
                "JSProgram" : "JSProgram",
                "URL" : "URL"
            }
        }
        PackageQueryDb(CreateOperation(), Package.from_dict(package)).execute()
        # update the package
        package['data'] = {
                "Content" : "NewContent",
                "JSProgram" : "NewJSProgram",
                "URL" : "NewURL"
            }
        response = self.client.open(
            f"/package/{package['metadata']['ID']}",
            method='PUT',
            headers={},
            data=json.dumps(package),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # get package from DB
        data = PackageQueryDb(ReadOperation(), Package.from_dict(package)).execute().to_dict()
        assert(package == data)

    def test_packages_list(self):
        """Test case for packages_list

        Get packages
        """
        # insert packages
        for i in range(0, 5):
            PackageQueryDb(CreateOperation(), Package.from_dict({
                "metadata" : {
                    "Version" : "1.2.3",
                    "ID" : f"package_{i}",
                    "Name" : f"Package # {i}"
                },
                "data" : {
                    "Content" : f"fedc0973923ba23948efff",
                    "JSProgram" : "exit()",
                    "URL" : f"https://url.to.package_{i}"
                }
            })).execute()
        package_query = [
            {
                # "Version" : "1.2.3",
                "Version" : "1.2.2-2.1.0",
                # "Version" : "^1.2.3",
                # "Version" : "~1.2.0",
                "Name" : "*"
            }
        ]
        response = self.client.open(
            '/packages',
            method='GET',
            headers={},
            data=json.dumps(package_query),
            content_type='application/json',
            query_string=[('offset', 0)]
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registry_reset(self):
        """Test case for registry_reset


        """
        # insert package into DB
        package = {
            "metadata" : {
                "Version" : "1.2.3",
                "ID" : "ID",
                "Name" : "Name"
            },
            "data" : {
                "Content" : "Content",
                "JSProgram" : "JSProgram",
                "URL" : "URL"
            }
        }
        PackageQueryDb(CreateOperation(), Package.from_dict(package)).execute()
        # send the request
        response = self.client.open(
            '/reset',
            method='DELETE',
            headers={})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # try to get package from DB
        data = PackageQueryDb(ReadOperation(), Package.from_dict(package)).execute()
        assert (data == None)


if __name__ == '__main__':
    unittest.main()
