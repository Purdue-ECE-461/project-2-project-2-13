from query_handler.operations.base_operation_ import Operation

class SearchOperation(Operation):
    def __init__(self, method=None, value=None):
        self.method = method
        self.value = value