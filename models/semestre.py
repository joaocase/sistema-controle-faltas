from models.cadeira import Cadeira

class Semestre:
    def __init__(self, identificador):
        self.identificador = identificador
        self.cadeiras = {}


    def adicionar_cadeira(self, cadeira):
        if cadeira.nome not in self.cadeiras:
            self.cadeiras[cadeira.nome] = cadeira
            return True
        return False


    def listar_cadeiras(self):
        return list(self.cadeiras.values())
