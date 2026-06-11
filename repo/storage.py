import json
import os
import shutil
from datetime import datetime

class StorageJSON:
    def __init__(self, arquivo='historico.json'):
        self.arquivo = arquivo


    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    
                    if not isinstance(dados, dict):
                        raise TypeError("O formato raiz do JSON foi corrompido (não é um dicionário).")
                        
                    return dados
            except Exception as e:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_base, extensao = os.path.splitext(self.arquivo)
                arquivo_backup = f"{nome_base}_corrompido_{timestamp}{extensao}"
                
                shutil.copy(self.arquivo, arquivo_backup)
                print("\n🚨 ALERTA CRÍTICO DE BANCO DE DADOS 🚨")
                print(f"O arquivo de salvamento estava corrompido. Backup salvo como: '{arquivo_backup}'.")
                print("Iniciando o sistema com um banco de dados em branco...\n")
                
        return {"semestre_atual": "", "semestres": {}}


    def salvar(self, dados):
        arquivo_temporario = self.arquivo + '.tmp'
        try:
            with open(arquivo_temporario, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            
            os.replace(arquivo_temporario, self.arquivo)
            return True
            
        except Exception as e:
            print(f"\n❌ ERRO CRÍTICO NO SISTEMA DE ARQUIVOS: Não foi possível salvar ({e})")
            if os.path.exists(arquivo_temporario):
                os.remove(arquivo_temporario)
            return False
