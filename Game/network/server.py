class MockServer:
    def __init__(self):
        self.clients = 1

    def tick(self):
        return {"clients": self.clients, "status": "ok"}
