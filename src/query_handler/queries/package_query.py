import json

import db
from openapi_server.models.package import Package
from query_handler.operations.create_operation import CreateOperation
from query_handler.operations.delete_operation import DeleteOperation
from query_handler.operations.read_operation import ReadOperation
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
        elif isinstance(operation, DeleteOperation):
            if (resource is None):
                db.reset('package')
            else:
                db.set('package', resource.metadata.id, None)
            return None
        else:
            raise TypeError(f'unexpected operation type `{type(operation)}`')
