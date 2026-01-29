from datetime import date
from ui import *

# Dados mockados
# Nome | Curso | Estrelhas/Acertos | Dia que fez
aluno_1 = ("João", "Comunicação", 50, "2026-01-27")
aluno_2 = ("Maria", "Lógica", 19, "2026-01-29")
aluno_3 = ("Carla", "Organização no Trabalho", 26, "2026-01-27")
aluno_4 = ("Adriano", "Comunicação", 10, "2026-01-29")
aluno_5 = ("Gustavo", "Lógica", 5, "2026-01-27")
aluno_6 = ("Letícia", "Tecnologia", 18, "2026-01-27")
aluno_7 = ("Marcos", "Organização no Trabalho", 44, "2026-01-27")
aluno_8 = ("Douglas", "Tecnologia", 36, "2026-01-29")

alunos_atividades = [aluno_1, aluno_2, aluno_3, aluno_4, aluno_5, aluno_6, aluno_7, aluno_8]


#((total_acertos) / (quantidade_alunos * quantidade_questoes)) * 100

# Menu do coordenador
while True:
    clear()
    print(f"Selecione uma opção:")
    print(f"\n1. Cadastrar novo aluno"
        f"\n2. Ver ranking das turmas"
        f"\n3. Ver atividades realizadas"
        f"\n4. Ver desempenho por curso"
        f"\n5. Sair")
    choice = input("> ")

    match choice:
        case "":
            print("\nO campo não pode ficar vazio!")
            call_to_action_clear()
            continue
        case "1":
            print("Cadastrar novo aluno")
        case "2":
            # Listar nome e pontuação de cada aluno por curso
            print("\nVer ranking das turma")
            while True:
                print("\n1. Para ver a lista de alunos e ranking")
                print("2. Para sair")

                opcao = input("\nAdicione a opção desejada: ")

                match opcao:
                    case "1":
                        if not alunos_atividades:
                            print("Não tem nenhum aluno cadastrado.")
                        else:
                            ranking = sorted(alunos_atividades, key=lambda estrelhas: estrelhas[2], reverse=True)
                            print("\n🏆 Ranking de Alunos 🏆")
                            for item in ranking:
                                print(f"Nome: {item[0]} | Curso: {item[1]} | Estrelas: {item[2]}")

                    case "2":
                        print("Encerando o programa.")
                        break

                    case _:
                        print("Opção inválida.")

            call_to_action_clear()
            continue
        case "3":
            # Listar, comparando a data de hoje com a data de quando foi feita a atividade
                # Por curso
            print("\nVer atividades realizadas")
            call_to_action_clear()
            continue
        case "4":
            # Segundo menu
                # Selecionar o curso
            print("\nVer desempenho por curso")
            call_to_action_clear()
            continue
        case "5":
            break
        case _:
            print("\nOpção inválida!")
            call_to_action_clear()
            continue
