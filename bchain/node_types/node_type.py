
class NodeType:

    def __init__(self):
        self.VIEW_PERMISSION = True
        self.PASSPORT_PERMISSION = False
        self.BORDER_PERMISSION = False
        self.VISA_PERMISSION = False

class GovernmentNodeType(NodeType):

    def __init__(self):
        super().__init__()
        self.PASSPORT_PERMISSION = True
        self.VISA_PERMISSION = True

class BorderControlNodeType(NodeType):

    def __init__(self):
        super().__init__()
        self.BORDER_PERMISSION = True

class EnforcementNodeType(NodeType):

    def __init__(self):
        super().__init__()

class APINodeType(NodeType):

    def __init__(self):
        super().__init__()