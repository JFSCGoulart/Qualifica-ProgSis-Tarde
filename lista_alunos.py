alunos = []

while True:
    print("\n1. Para adicionar alunos")
    print("2. Para ver a lista de alunos e ranking")
    print("3. Para sair")

    opcao = input("\nAdicione a opção desejada: ")

    match opcao:
        case "1":
            while True:
                nome_aluno = input("Adicione o nome do aluno: ")
                
                try:
                    qtd_de_estrelas = int(input("Adicione a quantidade de acertos do aluno: "))
                except ValueError:
                    print("Digite apenas números!")
                    continue

                # salva nome + estrelas juntos
                alunos.append((nome_aluno, qtd_de_estrelas))

                stop = input("Deseja adicionar mais alunos? (s/n): ").lower()
                if stop != "s":
                    break

        case "2":
            if not alunos:
                print("Não tem nenhum aluno cadastrado.")
            else:
                ranking = sorted(alunos, key=lambda aluno: aluno[1], reverse=True)

                print("\n🏆 Ranking de Alunos 🏆")
                for posicao, aluno in enumerate(ranking, start=1):
                    print(f"{posicao}º lugar - {aluno[0]} | Estrelas: {aluno[1]}")

        case "3":
            print("Encerando o programa.")
            break

        case _:
            print("Opção inválida.")

