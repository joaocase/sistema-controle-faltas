from models.base_dados import BaseDados

class MenuConsole:
    def __init__(self):
        self.bd = BaseDados()


    def iniciar(self):
        try:
            if not self.bd.current_semester:
                print("🎉 Bem-vindo ao Sistema Acadêmico!")
                semestre = input("Digite o semestre atual (ex: 2026.1): ").strip()
                
                while not semestre:
                    print("❌ Entrada inválida. O semestre não pode ser vazio.")
                    semestre = input("Digite o semestre atual (ex: 2026.1): ").strip()
                
                try:
                    self.bd.definir_current_semester(semestre)
                except ValueError as e:
                    print(f"\n❌ ERRO FATAL: {e}")
                    return

            while True:
                print(f"\n[ Painel Acadêmico | Semestre: {self.bd.current_semester} ]")
                print("1. Ver resumo de faltas")
                print("2. Lançar nova falta")
                print("3. Cadastrar nova cadeira")
                print("4. Excluir cadeira")
                print("5. Mudar de semestre / Iniciar novo")
                print("6. Sair")
                
                opcao = input("Opção: ").strip()
                
                if opcao == '1':
                    self._exibir_resumo()
                elif opcao == '2':
                    self._lancar_falta()
                elif opcao == '3':
                    self._cadastrar_cadeira()
                elif opcao == '4':
                    self._excluir_cadeira()
                elif opcao == '5':
                    self._mudar_semestre()
                elif opcao == '6':
                    print("\n👋 Encerrando...")
                    break
                else:
                    print("❌ Opção inválida.")
                    
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ Interrupção de sistema detectada. Encerrando o sistema em segurança. Até logo!")
            return


    def _exibir_resumo(self):
        cadeiras = self.bd.obter_cadeiras_do_semestre()
        print(f"\n=== RESUMO: {self.bd.current_semester} ===")
        if not cadeiras:
            print("Nenhuma cadeira cadastrada.")
            return
            
        for c in cadeiras:
            print(f"\n📘 {c.nome} ({c.carga_horaria}h)")
            print(f"   Status: {c.obter_status()}")
            print(f"   Faltas: {c.faltas_horas}h / Limite: {int(c.limite_faltas)}h")


    def _lancar_falta(self):
        cadeiras = self.bd.obter_cadeiras_do_semestre()
        if not cadeiras:
            return print("\n❌ Cadastre uma cadeira primeiro.")

        print("\nSelecione a cadeira (Será computada a falta do dia inteiro/4h):")
        for i, c in enumerate(cadeiras, 1):
            print(f"{i}. {c.nome}")
        
        entrada_idx = input("Número da cadeira: ").strip()
        if not entrada_idx.isdigit():
            return print("❌ Entrada inválida. Digite apenas o número.")
            
        idx = int(entrada_idx) - 1
        if not (0 <= idx < len(cadeiras)):
            return print("❌ Erro: Número de cadeira inexistente na lista.")

        cadeira_alvo = cadeiras[idx]

        nome_cadeira = cadeira_alvo.nome

        horas = cadeira_alvo.HORAS_POR_DIA 

        try:
            if self.bd.registrar_falta(nome_cadeira, horas):
                print(f"✅ Falta registrada! (+{horas}h adicionadas em {nome_cadeira})")

                print("-" * 40)
                print(f"📊 NOVO STATUS: {cadeira_alvo.obter_status()}")
                if cadeira_alvo.horas_restantes >= 0:
                    print(f"⏳ Saldo restante: Você ainda pode faltar {cadeira_alvo.horas_restantes}h antes de reprovar.")
                print("-" * 40)

            else:
                print("❌ Erro: Cadeira não encontrada no banco de dados.")
        except ValueError as e:
            print(f"❌ Erro de Regra de Negócio: {e}")


    def _cadastrar_cadeira(self):
        nome = input("\nNome da Cadeira: ").strip().upper()
        
        if not nome:
            return print("❌ O nome da cadeira não pode ser vazio.")
            
        entrada_ch = input("Carga horária total (ex: 60): ").strip()
        if not entrada_ch.isdigit():
            return print("❌ Carga horária inválida. Digite apenas números.")
            
        ch = int(entrada_ch)
        
        if ch <= 0:
            return print("❌ Carga horária deve ser maior que zero.")
            
        try:
            if self.bd.cadastrar_cadeira(nome, ch):
                print("✅ Cadeira cadastrada!")
            else:
                print("❌ Cadeira já existe neste semestre.")
        except ValueError as e:
            print(f"❌ Erro de Regra de Negócio: {e}")


    def _excluir_cadeira(self):
        cadeiras = self.bd.obter_cadeiras_do_semestre()
        if not cadeiras:
            return print("\n❌ Nenhuma cadeira para excluir.")

        print("\nSelecione a cadeira que deseja EXCLUIR:")
        for i, c in enumerate(cadeiras, 1):
            print(f"{i}. {c.nome}")
        
        entrada_idx = input("Número da cadeira para deletar: ").strip()
        if not entrada_idx.isdigit():
            return print("❌ Entrada inválida. Digite apenas o número.")
            
        idx = int(entrada_idx) - 1
        if not (0 <= idx < len(cadeiras)):
            return print("❌ Erro: Número inexistente na lista.")

        nome_cadeira = cadeiras[idx].nome
        confirmacao = input(f"⚠️ Tem certeza que deseja apagar a cadeira '{nome_cadeira}' e todo o seu histórico? (s/n): ").strip().lower()
        
        if confirmacao == 's':
            try:
                if self.bd.excluir_cadeira(nome_cadeira):
                    print(f"✅ Cadeira '{nome_cadeira}' excluída com sucesso!")
                else:
                    print("❌ Erro ao tentar excluir a cadeira.")
            except ValueError as e:
                print(f"❌ ERRO DE SISTEMA: {e}")
        else:
            print("✅ Operação cancelada. A cadeira foi mantida.")


    def _mudar_semestre(self):
        novo_semestre = input("\nDigite o identificador do novo semestre (ex: 2026.2): ").strip()
        
        if not novo_semestre:
            return print("❌ O semestre não pode ser vazio.")
            
        if novo_semestre == self.bd.current_semester:
            return print(f"⚠️ Você já está no semestre '{novo_semestre}'. Nenhuma mudança foi feita.")

        try:
            self.bd.definir_current_semester(novo_semestre)
            print(f"✅ Semestre alterado para '{novo_semestre}' com sucesso!")
            print("As cadeiras do semestre anterior estão salvas com segurança no histórico.")
        except ValueError as e:
            print(f"\n❌ ERRO DE SISTEMA: {e}")
