class Nodo:
    def __init__(self, data=0, peso=0.0):
        self.data = data
        self.peso = peso
        self.link = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_peso(self):
        return self.peso

    def set_peso(self, peso):
        self.peso = peso

    def get_link(self):
        return self.link

    def set_link(self, link):
        self.link = link
    