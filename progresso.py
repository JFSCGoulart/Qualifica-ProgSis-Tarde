from ui import *


while True:
    clear()
    print(f"Selecione uma opção:")
    print(f"\n1. Ver ranking das turma"
        f"\n2. Ver atividades realizadas"
        f"\n3. Ver desempenho por curso"
        f"\n4. Sair")
    choice = input("> ")

    if choice == "":
        print("\nO campo não pode ficar vazio!")
        call_to_action_clear()
        continue
    elif choice == "1":
        # Listar nome e pontuação de cada aluno por curso
        print("\nVer ranking das turma")
        call_to_action_clear()
        continue
        
    elif choice == "2":
        # Listar, comparando a data de hoje com a data de quando foi feita a atividade
            # Por curso
        print("\nVer atividades realizadas")
        call_to_action_clear()
        continue
    elif choice == "3":
        # Segundo menu
            # Selecionar o curso
        print("\nVer desempenho por curso")
        call_to_action_clear()
        continue
    elif choice == "4":
        break
    else:
        print("\nOpção inválida!")
        call_to_action_clear()
        continue
