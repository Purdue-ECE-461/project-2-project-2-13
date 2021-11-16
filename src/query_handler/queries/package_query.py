import json

import db
from openapi_server.models.package import Package
from query_handler.operations.create_operation import CreateOperation
from query_handler.operations.delete_operation import DeleteOperation
from query_handler.operations.read_operation import ReadOperation
from query_handler.queries.base_query_ import Query


class PackageQuery(Query):
    def execute(self):
        package: Package = self.resource
        operation = self.operation
        if isinstance(operation, CreateOperation):
            db.set('package', package.metadata.id, json.dumps(package.to_dict()))
            return package
        elif isinstance(operation, ReadOperation):
            return db.get('package', package.metadata.id)
        elif isinstance(operation, DeleteOperation):
            return db.set('package', package.metadata.id, None)
        else:
            raise TypeError(f'unexpected operation type `{type(operation)}`')
