import json
import logging

import db
from openapi_server.models.package import Package
from openapi_server.models.package_metadata import PackageMetadata
from query_handler.operations.create_operation import CreateOperation
from query_handler.operations.delete_operation import DeleteOperation
from query_handler.operations.read_operation import ReadOperation
from query_handler.operations.search_operation import SearchOperation
from query_handler.operations.update_operation import UpdateOperation
from query_handler.queries.base_query_ import Query


class PackageQuery(Query):
    def execute(self):
        resource = self.resource
        operation = self.operation
        if isinstance(operation, CreateOperation):
            db.set('package', resource.metadata.id, resource.to_dict())
            return resource
        elif isinstance(operation, UpdateOperation):
            # get current package
            data = db.get('package', resource.metadata.id)
            if data is None:
                return None
            current = Package.from_dict(data)
            # replace package data with new data
            current.data = resource.data
            db.set('package', resource.metadata.id, current.to_dict())
            return current
        elif isinstance(operation, ReadOperation):
            data = db.get('package', resource.metadata.id)
            return None if data is None else Package.from_dict(data)
        elif isinstance(operation, SearchOperation):
            if (operation.method == 'byName'):
                name = operation.value
                packages = db.get('package')
                for id in packages:
                    temp = Package.from_dict(packages[id])
                    if (temp.metadata.name == name):
                        return PackageMetadata.from_dict(packages[id]['metadata'])
                logging.error(f'package with name \'{name}\' not found')
            elif (operation.method == 'list'):
                offset = int(operation.value)
                results = []
                packages = db.get('package')
                for idx, id in enumerate(packages, offset):
                    if (len(results) < 10):
                        results.append(PackageMetadata.from_dict(packages[id]['metadata']))
                return results
            else:
                logging.error(f'operation method \'{operation.method}\' is not supported')
            return None
        elif isinstance(operation, DeleteOperation):
            if (resource is None):
                db.reset('package')
            else:
                db.set('package', resource.metadata.id, None)
            return None
        else:
            raise TypeError(f'unexpected operation type `{type(operation)}`')
