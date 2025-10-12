class ResourceManager:
    def __init__(self):
        self.ressourcen = 0

    def add_ressourcen(self, amount):
        self.ressourcen += amount

    def subtract_ressourcen(self, amount):
        if self.ressourcen >= amount:
            self.ressourcen -= amount
            return True
        return False
