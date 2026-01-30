from datetime import date
from progresso_funcoes import *
from ui import *

# Dados mockados
# Nome | Curso | Quantas atividades fez | Estrelhas/Acertos | Dia que fez
aluno_1 = ("João", "Comunicação", 60, 37, "2026-01-27")
aluno_2 = ("Maria", "Lógica", 46, 19, "2026-01-29")
aluno_3 = ("Carla", "Organização no Trabalho", 32, 26, "2026-01-27")
aluno_4 = ("Adriano", "Comunicação", 18, 10, "2026-01-29")
aluno_5 = ("Gustavo", "Lógica", 15, 5, "2026-01-27")
aluno_6 = ("Letícia", "Tecnologia", 20, 18, "2026-01-27")
aluno_7 = ("Marcos", "Organização no Trabalho", 53, 44, "2026-01-27")
aluno_8 = ("Douglas", "Tecnologia", 44, 36, "2026-01-29")

alunos_atividades = [aluno_1, aluno_2, aluno_3, aluno_4, aluno_5, aluno_6, aluno_7, aluno_8]

# Menu do coordenador
while True:
    clear()
    menu_title("Coordenador")
    print("\nSelecione uma opção:")
    print("1. Cadastrar novo aluno"
        "\n2. Ver ranking das turmas"
        "\n3. Ver atividades realizadas"
        "\n4. Ver desempenho por curso"
        "\n5. Sair")
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
            while True:
                clear()
                menu_title("Ver ranking das turmas")
                print(f"\nSelecione uma opção:")
                print("1. Para ver a lista de alunos e ranking"
                      "\n2. Voltar")
                opcao = input("> ")

                match opcao:
                    case "1":
                        if not alunos_atividades:
                            print("Não tem nenhum aluno cadastrado.")
                        else:
                            clear()
                            menu_title("Ranking das turmas")
                            ranquear_alunos(alunos_atividades, "Comunicação")
                            ranquear_alunos(alunos_atividades, "Lógica")
                            ranquear_alunos(alunos_atividades, "Organização no Trabalho")
                            ranquear_alunos(alunos_atividades, "Tecnologia")
                                    
                            call_to_action_clear()
                    case "2":
                        break
                    case _:
                        print("Opção inválida.")
            if opcao == "2":
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
                # ((total_acertos) / (quantidade_alunos * quantidade_questoes)) * 100
            print("\nVer desempenho por curso")
            call_to_action_clear()
            continue
        case "5":
            break
        case _:
            print("\nOpção inválida!")
            call_to_action_clear()
            continue
