from models.semestre import Semestre
from models.cadeira import Cadeira
from repo.storage import StorageJSON

class BaseDados:
    def __init__(self):
        self.storage = StorageJSON()
        self.semesters = {}
        self.current_semester = ""
        self._inicializar_dados()


    def _inicializar_dados(self):
        dados = self.storage.carregar()
        
        self.current_semester = str(dados.get("semestre_atual", "")).strip()
        
        semestres_dict = dados.get("semestres", {})

        if not isinstance(semestres_dict, dict):
            semestres_dict = {}

        for id_semestre, cadeiras_dict in semestres_dict.items():
            id_semestre = str(id_semestre).strip()
            if not id_semestre:
                continue
                
            novo_semestre = Semestre(id_semestre)
            
            if isinstance(cadeiras_dict, dict):
                for nome, info in cadeiras_dict.items():
                    nome = str(nome).strip().upper() 
                    try:
                        if not isinstance(info, dict):
                            raise TypeError("Estrutura interna da cadeira corrompida.")
                            
                        carga = info.get("carga_horaria", 0)
                        faltas = info.get("faltas_horas", 0)
                        cadeira = Cadeira(nome, carga, faltas)
                        novo_semestre.adicionar_cadeira(cadeira)
                    except (ValueError, TypeError):
                        print(f"⚠️ AVISO: A cadeira '{nome}' no semestre '{id_semestre}' contém dados inválidos e foi ignorada.")
                        
            self.semesters[id_semestre] = novo_semestre

        if self.current_semester and self.current_semester not in self.semesters:
            self.semesters[self.current_semester] = Semestre(self.current_semester)


    def salvar_estado(self):
        dados_para_salvar = {"semestre_atual": self.current_semester, "semestres": {}}
        for id_sem, obj_semestre in self.semesters.items():
            dados_para_salvar["semestres"][id_sem] = {}
            for c in obj_semestre.listar_cadeiras():
                dados_para_salvar["semestres"][id_sem][c.nome] = c.para_dicionario()
                
        if not self.storage.salvar(dados_para_salvar):
            raise IOError("Falha na sincronização com o banco de dados físico.")


    def definir_current_semester(self, identificador):
        semestre_anterior = self.current_semester
        novo_criado = False
        
        if identificador not in self.semesters:
            self.semesters[identificador] = Semestre(identificador)
            novo_criado = True
            
        self.current_semester = identificador
        
        try:
            self.salvar_estado()
        except IOError:
            self.current_semester = semestre_anterior
            if novo_criado:
                del self.semesters[identificador]
            raise ValueError("Erro de I/O: Não foi possível criar o semestre no disco. Operação revertida.")


    def cadastrar_cadeira(self, nome, carga_horaria):
        nova_cadeira = Cadeira(nome, carga_horaria)
        semestre_ativo = self.semesters[self.current_semester]
        
        if semestre_ativo.adicionar_cadeira(nova_cadeira):
            try:
                self.salvar_estado()
                return True
            except IOError:
                del semestre_ativo.cadeiras[nome]
                raise ValueError("Erro de I/O: A cadeira não pôde ser salva com segurança no disco. Operação revertida.")
        return False


    def registrar_falta(self, nome_cadeira, horas):
        if self.current_semester in self.semesters:
            semestre_ativo = self.semesters[self.current_semester]
            if nome_cadeira in semestre_ativo.cadeiras:
                cadeira = semestre_ativo.cadeiras[nome_cadeira]
                cadeira.adicionar_falta(horas)
                
                try:
                    self.salvar_estado()
                    return True
                except IOError:
                    cadeira.faltas_horas -= horas
                    raise ValueError("Erro de I/O: A falta não pôde ser salva com segurança no disco. Operação revertida.")
        return False


    def excluir_cadeira(self, nome_cadeira):
        if self.current_semester in self.semesters:
            semestre_ativo = self.semesters[self.current_semester]
            if nome_cadeira in semestre_ativo.cadeiras:
                cadeira_removida = semestre_ativo.cadeiras.pop(nome_cadeira)
                
                try:
                    self.salvar_estado()
                    return True
                except IOError:
                    semestre_ativo.cadeiras[nome_cadeira] = cadeira_removida
                    raise ValueError("Erro de I/O: Não foi possível excluir no disco. Operação revertida.")
        return False

    def obter_cadeiras_do_semestre(self):
        if self.current_semester in self.semesters:
            return self.semesters[self.current_semester].listar_cadeiras()
        return []
