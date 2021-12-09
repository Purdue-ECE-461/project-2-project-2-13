from query_handler.operations.base_operation_ import Operation

class SearchOperation(Operation):
    def __init__(self, query=None, offset=0):
        self.query = query
        self.offset = offset