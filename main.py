import uuid

class Aluno:
    def __init__(self, uuid, nome):
        self.uuid = uuid
        self.nome = nome
        self.disciplinas = []
        self.notas = {}

    def associar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)

    def resultado_disciplina(self, disciplina):
        notas = self.notas.get(disciplina, [])
        if not notas:
            return 0.0
        return sum(notas) / len(notas)
    
    def media_geral(self):
        if not self.notas:
            return 0.0
        
        total = sum(self.resultado_disciplina(disc) for disc in self.notas)
        return total / len(self.notas)
    
class Disciplinas: 
    def __init__(self, nome):
        self.nome = nome
        self.alunos = []
    
    def associar_aluno(self, aluno):
        self.alunos.append(aluno)

def PrintMenu():
    print("=" * 40)
    print("\t\033[1;33mSISTEMA ACADEMICO\033[0m")
    print("=" * 40)
    print("\n\033[1mEscolha sua opção:\033[0m\n")
    print("(1) \033[1;32mCadastrar\033[0m Aluno")
    print("(2) \033[1;32mCadastrar\033[0m Disciplina")
    print("(3) Associar aluno a disciplina")
    print("(4) \033[1;32mCadastrar\033[0m Notas")
    print("(5) Emitir relatório de disciplinas")
    print("(6) Emitir relatório de alunos")
    print("(7) \033[1;31mSair\033[0m")
    print("(8) \033[1;34mExibir menu\033[0m")
    print("\n" + "=" * 40)

class Server:
    def __init__(self):
        self.alunos = []
        self.disciplinas = []

    def __cadastrar_aluno(self):
        if len(self.alunos) >= 5:
            print("\033[1;31mLimite máximo de 5 alunos atingido!\033[0m")
            return
        
        nome = input("Digite o nome do aluno: ")
        aluno_uuid = uuid.uuid4()
        aluno = Aluno(str(aluno_uuid), nome)
        self.alunos.append(aluno)
        print(f"\n\033[1;32mAluno '{nome}' cadastrado com sucesso!\033[0m\n")

    def __cadastrar_disciplina(self):
        if len(self.disciplinas) >= 2:
            print("\033[1;31mLimite máximo de 2 disciplinas atingido!\033[0m")
            return

        nome = input("Digite o nome da disciplina: ")
        disciplina = Disciplinas(nome)
        self.disciplinas.append(disciplina)
        print(f"\n\033[1;32mDisciplina '{nome}' cadastrada com sucesso!\033[0m\n")

    def __associar_aluno_disciplina(self):
        if not self.alunos or not self.disciplinas:
            print("\033[1;31mÉ necessário ter alunos e disciplinas cadastrados!\033[0m")
            return
        
        print("\n\033[1mAlunos disponíveis:\033[0m")
        for aluno in self.alunos:
            print(f"Prontuário: {aluno.uuid} | Nome: {aluno.nome}")

        aluno_uuid = input("\nDigite o prontuário do aluno que deseja associar: ")

        print("\n\033[1mDisciplinas disponíveis:\033[0m")
        for disciplina in self.disciplinas:
            print(f"- {disciplina.nome}")

        disciplina_nome = input("Digite o nome da disciplina: ")

        for aluno in self.alunos:
            if str(aluno.uuid) == aluno_uuid:
                for disciplina in self.disciplinas:
                    if disciplina.nome == disciplina_nome:
                        if len(disciplina.alunos) >= 4:
                            print("\033[1;31mLimite de 4 alunos nesta disciplina atingido!\033[0m")
                            return
                        
                        if aluno.uuid in disciplina.alunos:
                            print("\033[1;31mAluno já matriculado nesta disciplina!\033[0m")
                            return

                        disciplina.associar_aluno(aluno.uuid)
                        aluno.associar_disciplina(disciplina.nome)
                        print(f"\n\033[1;32mAluno associado com sucesso!\033[0m\n")
                        return
        print("\033[1;31mAluno ou disciplina não encontrados.\033[0m")
                    
    def __cadastrar_notas(self):
        if not self.alunos or not self.disciplinas:
            print("\033[1;31mNenhum aluno/disciplina cadastrado!\033[0m")
            return

        print("\n\033[1mAlunos disponíveis:\033[0m")
        for aluno in self.alunos:
            print(f"Prontuário: {aluno.uuid} | Nome: {aluno.nome}")
            
        aluno_uuid = input("\nDigite o prontuário do aluno: ")

    
        for aluno in self.alunos:
            if str(aluno.uuid) == aluno_uuid:
                for disciplina in aluno.disciplinas:
                    print(f"- {disciplina}")

                disciplina_nome = input("Digite o nome da disciplina: ")

                if disciplina_nome not in aluno.disciplinas:
                    print("\033[1;31mO aluno não está matriculado nesta disciplina.\033[0m")
                    return
                
                aluno.notas[disciplina_nome] = []
                print(f"Lançando notas para {aluno.nome} em {disciplina_nome}:")
                for i in range(4):
                    while True:
                        try:
                            nota = float(input(f"Digite a nota {i+1}: "))
                            if 0 <= nota <= 10:
                                aluno.notas[disciplina_nome].append(nota)
                                break
                            else:
                                print("\033[1;31mA nota deve ser entre 0 e 10!\033[0m")
                        except ValueError:
                            print("\033[1;31mEntrada inválida! Digite um número.\033[0m")
                print(f"\n\033[1;32mNotas cadastradas com sucesso!\033[0m\n")
                return

    def __emitir_relatorio_disciplinas(self):   
        if not self.disciplinas:
            print("\033[1;31mNenhuma disciplina cadastrada!\033[0m")
            return

        print("\n\033[1mDIÁRIO DE DISCIPLINAS:\033[0m\n")
        mapa_alunos = {str(aluno.uuid): aluno for aluno in self.alunos}

        for disciplina in self.disciplinas:
            print(f"Disciplina: {disciplina.nome}")
            print("Alunos matriculados:")
            
            total_notas = 0
            qtd_alunos = 0

            if not disciplina.alunos:
                print("  (Nenhum aluno matriculado)")

            for aluno_uuid in disciplina.alunos:
                aluno = mapa_alunos.get(aluno_uuid)
                if aluno:
                    notas = aluno.notas.get(disciplina.nome, [])
                    media = aluno.resultado_disciplina(disciplina.nome)
                    print(f"- {aluno.nome} | Notas: {notas} | Média: {media:.2f}")
                    
                    total_notas += media
                    qtd_alunos += 1

            print("Media da disciplina: ", end="")         
            if qtd_alunos > 0:
                media_disciplina = total_notas / qtd_alunos
                print(f"{media_disciplina:.2f}")
            else:
                print("N/A")       
            print("-" * 40)

    def __emitir_relatorio_alunos(self):
        if not self.alunos:
            print("\033[1;31mNenhum aluno cadastrado!\033[0m")
            return

        print("\n\033[1mATESTADO DE MATRÍCULA:\033[0m\n")
        
        for aluno in self.alunos:
            print(f"Prontuário (UUID): {aluno.uuid}")
            print(f"Aluno: {aluno.nome}")
            print("Disciplinas:")
            
            if not aluno.disciplinas:
                print("  (Não matriculado em nenhuma disciplina)")

            for disciplina_nome in aluno.disciplinas:
                notas = aluno.notas.get(disciplina_nome, [])
                media = aluno.resultado_disciplina(disciplina_nome)
                status = "Aprovado" if media >= 6.0 and len(notas) == 4 else "Reprovado"
                print(f"- {disciplina_nome} | Notas: {notas} | Média: {media:.2f} | Resultado: {status}")
            
            media_geral = aluno.media_geral()
            print(f"Média geral do aluno: {media_geral:.2f}")
            print("=" * 40)

    def run(self):
        PrintMenu()
        while True:
            opcao = input("Digite a opção desejada: ")
            if opcao == "8":
                print("\n\n")
                PrintMenu()
            elif opcao == "1":
                self.__cadastrar_aluno()
            elif opcao == "2":
                self.__cadastrar_disciplina()
            elif opcao == "3":
                self.__associar_aluno_disciplina()
            elif opcao == "4":
                self.__cadastrar_notas()
            elif opcao == "5":
                self.__emitir_relatorio_disciplinas()
            elif opcao == "6":
                self.__emitir_relatorio_alunos()
            elif opcao == "7":
                print("\n\033[1;31mSaindo do sistema...\033[0m\n")
                break
            else:
                print("\n\033[1;31mOpção inválida! Digite novamente.\033[0m\n")

app = Server()
app.run()
