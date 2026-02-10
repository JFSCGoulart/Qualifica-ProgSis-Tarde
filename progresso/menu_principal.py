from ui import (
    clear,
    menu_feedback,
    call_to_action_clear,
    render_menu_coordenador
)

from progresso.menu_administracao import menu_administracao

from progresso.menu_desempenho import (
    menu_ver_ranking,
    menu_ver_tentativas_de_hoje,
    menu_ver_desempenho_por_curso
)

def rodar_menu_principal():
    while True:
        clear()
        render_menu_coordenador()
        choice = input("> ")

        match choice:
            case "1":
                menu_administracao()
            case "2":
                menu_ver_ranking()
            case "3":
                menu_ver_tentativas_de_hoje()
            case "4":
                menu_ver_desempenho_por_curso()
            case "5":
                menu_feedback("Serviço encerrado...")
                break
            case _:
                menu_feedback("Opção inválida!")
                call_to_action_clear()
