class MonitorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class AgentExistError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DeleteError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotCreateAgentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
