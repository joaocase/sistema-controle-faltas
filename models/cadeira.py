class Cadeira:
    HORAS_POR_DIA = 4

    def __init__(self, nome, carga_horaria, faltas_horas=0):
        if not nome or not str(nome).strip():
            raise ValueError("O nome da cadeira não pode ser vazio.")
            
        if int(carga_horaria) <= 0:
            raise ValueError("A carga horária deve ser maior que zero.")
        
        if int(faltas_horas) < 0:
            raise ValueError("O histórico de faltas não pode ser negativo.")
        
        if int(faltas_horas) > int(carga_horaria):
            raise ValueError("As faltas iniciais não podem ser maiores que a carga horária total.")

        self.nome = str(nome).strip()
        self.carga_horaria = int(carga_horaria)
        self.faltas_horas = int(faltas_horas)


    @property
    def limite_faltas(self):
        return int(self.carga_horaria * 0.25)


    @property
    def horas_restantes(self):
        return self.limite_faltas - self.faltas_horas


    def adicionar_falta(self, horas):
        if horas <= 0:
            raise ValueError("A quantidade de faltas adicionadas deve ser positiva.")

        if self.faltas_horas + horas > self.carga_horaria:
            raise ValueError(f"As faltas ({self.faltas_horas + horas}h) não podem exceder a carga total da cadeira ({self.carga_horaria}h).")

        self.faltas_horas += horas


    def obter_status(self):
        if self.faltas_horas > self.limite_faltas:
            return "REPROVADO POR FALTAS"
        elif self.horas_restantes < self.HORAS_POR_DIA:
            return "ALERTA MÁXIMO (Zero margem para faltar 1 dia!)"
        else:
            return "SEGURO"


    def para_dicionario(self):
        return {
            "carga_horaria": self.carga_horaria,
            "faltas_horas": self.faltas_horas
        }
