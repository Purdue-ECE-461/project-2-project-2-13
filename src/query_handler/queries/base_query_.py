from query_handler.operations.base_operation_ import Operation

class Query(object):
    def __init__(self, operation=None, resource=None):
        self.attribute_map = {
            'operation': 'Operation',
            'resource': 'Resource'
        }

        self._operation = operation
        self._resource = resource

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation):
        if operation is None:
            raise ValueError("Invalid value for `operation`, must not be `None`")
        if operation is not Operation:
            raise TypeError("Invalid type for `operation`, must be `Operation`")
        self._operation = operation