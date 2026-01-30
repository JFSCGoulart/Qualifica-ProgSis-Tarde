def ranquear_alunos(lista_alunos, nome_curso):

    exibiu_menu = False


    alunos_do_curso = [
        aluno for aluno in lista_alunos if aluno[1] == nome_curso
    ]

    ranking = sorted(alunos_do_curso, key=lambda aluno: aluno[3], reverse=True)
    
    for posicao, item in enumerate(ranking, start=1):
        if item[1] == nome_curso:
            if not exibiu_menu:
                print(f"\n--- Total de acerto em {nome_curso} ---")
                exibiu_menu = True
            print(
                f"Posição: {posicao}º | "
                f"Nome: {item[0]} | "
                f"Curso: {item[1]} | "
                f"Questões feitas: {item[2]} | "
                f"Estrelas (acertos): {item[3]} | "
                f"Data: {item[4]}"
            )
