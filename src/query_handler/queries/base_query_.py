from abc import abstractclassmethod
from query_handler.operations.base_operation_ import Operation

class Query(object):
    def __init__(self, operation, resource=None):
        if operation is None:
            raise ValueError('operation cannot be `None`')
        self.operation = operation
        self.resource = resource

    @abstractclassmethod
    def execute(self):
        pass