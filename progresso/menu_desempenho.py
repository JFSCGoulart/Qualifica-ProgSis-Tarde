import progresso.repositorio_ranking as repositorio_ranking
from ui import *


def ver_ranking(nome_curso):
    clear()

    if not repositorio_ranking.existem_atividade_no_curso(nome_curso):
        menu_feedback("Nenhum aluno fez atividades desse curso ainda.")
        return

    menu_title(f"Ranking de {nome_curso}")
    resultado = repositorio_ranking.ranquear_alunos(nome_curso)

    if not resultado:
        menu_feedback(f"Nenhum aluno matriculado no curso de {nome_curso}.")
        return

    for posicao, (nome_usuario, feitas, acertadas) in enumerate(resultado, start=1):
        prefixo = "\n" if posicao == 1 else ""
        print(
            prefixo +
            f"Posição: {posicao}º | "
            f"Nome: {nome_usuario} | "
            f"Questões feitas: {feitas} | "
            f"Estrelas (acertos): {acertadas}"
        )


def menu_ver_ranking():
    while True:
        clear()
        render_menu_escolha_curso("VER RANKING DAS TURMAS")
        opcao = input("> ")

        match opcao:
            case "1":
                ver_ranking("Matemática")       
                call_to_action_clear()
            case "2":
                ver_ranking("Português")
                call_to_action_clear()
            case "3":
                ver_ranking("História")
                call_to_action_clear()
            case "4":
                ver_ranking("Geografia")
                call_to_action_clear()
            case "5":
                ver_ranking("Ciências")
                call_to_action_clear()
            case "6":
                return
            case _:
                menu_feedback("Opção inválida.")
                call_to_action_clear()


def ver_tentativas_de_hoje(nome_curso):
    clear()

    menu_title(f"Total de atividades realizadas hoje em {nome_curso}")
    linha = repositorio_ranking.total_atividades_hoje(nome_curso)

    quantidade_de_alunos, quantidade_atividades_feitas, _ultima_data = linha

    if quantidade_atividades_feitas == 0:
        menu_feedback("Hoje ninguém fez atividades nesse curso.")
        return

    aluno_str = "aluno" if quantidade_de_alunos == 1 else "alunos"
    acao_str = "fez" if quantidade_de_alunos == 1 else "fizeram"
    atividade_str = "atividade" if quantidade_atividades_feitas == 1 else "atividades"

    print(
        f"\nHoje, {quantidade_de_alunos} {aluno_str} {acao_str} "
        f"{quantidade_atividades_feitas} {atividade_str}."
    )


def menu_ver_tentativas_de_hoje():
    while True:
        clear()
        render_menu_escolha_curso("TOTAL DE ATIVIDADES FEITAS HOJE")
        opcao = input("> ")

        match opcao:
            case "1":
                ver_tentativas_de_hoje("Matemática")       
                call_to_action_clear()
            case "2":
                ver_tentativas_de_hoje("Português")
                call_to_action_clear()
            case "3":
                ver_tentativas_de_hoje("História")
                call_to_action_clear()
            case "4":
                ver_tentativas_de_hoje("Geografia")
                call_to_action_clear()
            case "5":
                ver_tentativas_de_hoje("Ciências")
                call_to_action_clear()
            case "6":
                return
            case _:
                menu_feedback("Opção inválida.")
                call_to_action_clear()


def ver_desempenho_por_curso(nome_curso):
    clear()

    menu_title(f"Desempenho em {nome_curso}")
    linha = repositorio_ranking.desempenho_por_curso(nome_curso)

    quant_matriculados, quant_questoes, quant_fizeram, total_acertos = linha

    if quant_matriculados == 0:
        menu_feedback(f"Nenhum aluno matriculado no curso {nome_curso}.")
        return

    if quant_questoes == 0:
        menu_feedback(f"Nenhuma atividade cadastrada no curso {nome_curso}.")
        return

    quant_nao_fizeram = quant_matriculados - quant_fizeram

    if quant_fizeram == 0:
        menu_feedback(f"{quant_matriculados} alunos matriculados, mas ninguém fez atividades nesse curso.")
        return

    resultado = (total_acertos / (quant_matriculados * quant_questoes)) * 100

    print(f"\n{resultado:.2f}% acertaram o módulo de {nome_curso}")
    print(f"Matriculados: {quant_matriculados} | Fizeram: {quant_fizeram} | Não fizeram: {quant_nao_fizeram}")


def menu_ver_desempenho_por_curso():
    while True:
        clear()
        render_menu_escolha_curso("DESEMPENHO POR CURSO")
        opcao = input("> ")

        match opcao:
            case "1":
                ver_desempenho_por_curso("Matemática")       
                call_to_action_clear()
            case "2":
                ver_desempenho_por_curso("Português")
                call_to_action_clear()
            case "3":
                ver_desempenho_por_curso("História")
                call_to_action_clear()
            case "4":
                ver_desempenho_por_curso("Geografia")
                call_to_action_clear()
            case "5":
                ver_desempenho_por_curso("Ciências")
                call_to_action_clear()
            case "6":
                return
            case _:
                menu_feedback("Opção inválida.")
                call_to_action_clear()
