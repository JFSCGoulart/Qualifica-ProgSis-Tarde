from datetime import date

def ranquear_alunos(lista_alunos, nome_curso):

    exibiu_menu = False

    alunos_do_curso = [
        aluno for aluno in lista_alunos if aluno[1] == nome_curso
    ]

    ranking = sorted(alunos_do_curso, key=lambda aluno: aluno[3], reverse=True)

    if alunos_do_curso:
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
    else:
        print(f"\n- Nenhum aluno cadastrado no curso {nome_curso}")

def total_atividades_hoje(lista_alunos, nome_curso):
    data_atual = date.today()
    
    alunos_filtrados = [
        aluno for aluno in lista_alunos
        if aluno[1] == nome_curso
        and aluno[4] == data_atual
    ]    

    quantidade = len(alunos_filtrados)

    if alunos_filtrados:
        total_atividades = sum(aluno[2] for aluno in alunos_filtrados)
        aluno_str = "aluno" if quantidade == 1 else "alunos"
        acao_str = "fez" if quantidade == 1 else "fizeram"
        atividade_str = "atividade" if total_atividades == 1 else "atividades"
        print(f"\n- {len(alunos_filtrados)} {aluno_str} {acao_str} um total de {total_atividades} {atividade_str} em {nome_curso}")
    else:
        print(f"\n- Nenhum aluno de {nome_curso} fez atividades hoje ({data_atual})")

def desempenho_por_curso(lista_alunos, nome_curso):
    alunos_do_curso = [
        aluno for aluno in lista_alunos if aluno[1] == nome_curso
    ]

    total_acertos = sum(aluno[3] for aluno in alunos_do_curso)
    quant_alunos = len(alunos_do_curso)
    quant_questoes = 100

    if alunos_do_curso:
        resultado = ((total_acertos) / (quant_alunos * quant_questoes)) * 100
        print(f"\n- {resultado}% acertaram o módulo de {nome_curso}")
    else:
        print(f"\n- Nenhum aluno cadastrado no curso {nome_curso}")
