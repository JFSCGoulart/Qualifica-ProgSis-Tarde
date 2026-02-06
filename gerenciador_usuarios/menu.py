from gerenciador_usuarios.modelos import Aluno, Coordenador, Professor

from gerenciador_usuarios.repositorio import (
    buscar_usuario_por_id_e_tipo,
    buscar_usuario_por_tipo,
    deletar_usuario,
    inserir_usuario,
)

from gerenciador_usuarios.validadores import formatar_cpf, validar_email
from gerenciador_usuarios.prompts import perguntar

from ui import (
    call_to_action_clear,
    clear,
    menu_error_success,
    render_menu_cadastrar_usuario,
    render_menu_coordenador,
    render_menu_remover_usuario,
    render_menu_tipo_usuario,
    render_menu_visualizar_usuario,
)


def cadastrar_usuarios(tipo_cls, tipo_num, label):
    def render():
        render_menu_cadastrar_usuario(label.upper())

    nome = email = cpf_formatado = None
    step = "nome"

    while True:
        clear()
        render()

        if step == "nome":
            nome = perguntar(
                f"\nNome completo do {label} (ou '<' pra voltar): ",
                redraw = render,
            )
            if nome is None:
                return
            step = "email"

        elif step == "email":
            email = perguntar(
                f"\nEmail do {label} {nome} (ou '<' pra voltar): ",
                redraw = render,
            )
            if email is None:
                step = "nome"
                continue

            if not validar_email(email):
                menu_error_success("Email inválido. Tente novamente.")
                call_to_action_clear()
                continue

            step = "cpf"

        elif step == "cpf":
            cpf_raw = perguntar(
                f"\nCPF do(a) {label} {nome} (somente números ou XXX.XXX.XXX-XX). "
                "Digite '<' pra voltar: ",
                redraw = render,
            )
            if cpf_raw is None:
                step = "email"
                continue

            cpf_formatado = formatar_cpf(cpf_raw)
            if cpf_formatado is None:
                menu_error_success("CPF inválido. Tente novamente.")
                call_to_action_clear()
                continue

            step = "senha"

        elif step == "senha":
            senha = perguntar(
                "\nDigite a senha (ou '<' pra voltar): ",
                secret = True,
                redraw = render,
            )
            if senha is None:
                step = "cpf"
                continue

            senha_confirmacao = perguntar(
                "\nDigite a senha novamente (ou '<' pra voltar): ",
                secret = True,
                redraw = render,
            )
            if senha_confirmacao is None:
                step = "senha"
                continue

            try:
                novo_user = tipo_cls(
                    nome,
                    email,
                    cpf_formatado,
                    senha,
                    senha_confirmacao,
                    tipo = tipo_num,
                )
            except ValueError as e:
                menu_error_success(str(e))
                call_to_action_clear()
                continue

            resultado = inserir_usuario(novo_user)

            if resultado is True:
                clear()
                menu_error_success("Cadastro realizado com sucesso!")
            elif resultado is False:
                menu_error_success("CPF ou email já cadastrado")
            else:
                menu_error_success("Erro crítico ao acessar o banco")

            while True:
                stop = input(f"\nDeseja adicionar mais {label}s? (s/n): ").strip().lower()

                if stop not in ("s", "n"):
                    menu_error_success("Resposta inválida. Digite 's' para sim ou 'n' para não.")
                    call_to_action_clear()
                    continue

                if stop == "n":
                    return

                nome = email = cpf_formatado = None
                step = "nome"
                break


def menu_cadastrar_usuarios():
    while True:
        clear()
        render_menu_tipo_usuario()
        escolha = input("> ").strip()

        match escolha:
            case "1":
                clear()
                cadastrar_usuarios(Aluno, 1, "aluno")
            case "2":
                clear()
                cadastrar_usuarios(Professor, 2, "professor")
            case "3":
                clear()
                cadastrar_usuarios(Coordenador, 3, "coordenador")
            case "4":
                return
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()
                continue


def visualizar_usuarios(tipo_num, label):
    resultado = buscar_usuario_por_tipo(tipo_num)

    if not resultado:
        menu_error_success(f"Nenhum {label.lower()} cadastrado.")
        return

    print(f"=== Lista de {label}s ===")
    for id, nome, email, cpf, *_ in resultado:
        print(f"ID: {id} | Nome: {nome} | Email: {email} | CPF: {cpf}")


def visualizar_usuario(id_usuario: int, tipo: int, label: str):
    resultado = buscar_usuario_por_id_e_tipo(id_usuario, tipo)

    if not resultado:
        return False

    id, nome, email, cpf, tipo_usuario = resultado
    print(f"=== {label.capitalize()} encontrado ===")
    print(f"ID: {id} | Nome: {nome} | Email: {email} | CPF: {cpf} | Tipo: {tipo_usuario}")
    return True


def menu_visualizar_usuarios():
    while True:
        render_menu_visualizar_usuario()
        escolha = input("> ").strip()

        match escolha:
            case "1":
                clear()
                visualizar_usuarios(1, "aluno")
                call_to_action_clear()
            case "2":
                clear()
                visualizar_usuarios(2, "professor")
                call_to_action_clear()
            case "3":
                clear()
                visualizar_usuarios(3, "coordenador")
                call_to_action_clear()
            case "4":
                return
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()
                continue


def remover_usuario(tipo_num: int, label: str) -> None:
    while True:
        clear()
        tem_usuarios = visualizar_usuarios(tipo_num, label)

        if not tem_usuarios:
            call_to_action_clear()
            return

        user_id_raw = input(f"\nDigite o ID do(a) {label} para deletar (ou '<' pra voltar): ").strip()

        if user_id_raw == "<":
            return

        if not user_id_raw.isdigit():
            menu_error_success("ID inválido. Digite um número ou '<' para voltar.")
            call_to_action_clear()
            continue

        id_usuario = int(user_id_raw)

        while True:
            clear()
            resultado = visualizar_usuario(id_usuario, tipo_num, label)

            if resultado is False:
                print(f"O ID {id_usuario} não está associado a nenhum {label} cadastrado.")
                call_to_action_clear()
                break

            confirm = input(f"\nTem certeza que deseja deletar o(a) {label} de ID {id_usuario}? (s/n): ").strip().lower()
            
            if confirm not in ("s", "n"):
                menu_error_success("Resposta inválida. Digite 's' para sim ou 'n' para não.")
                call_to_action_clear()
                continue

            if confirm == "n":
                break

            if confirm == "s":
                resultado = deletar_usuario(id_usuario, tipo_num)
                
                if resultado is True:
                    menu_error_success("Usuário deletado com sucesso!")
                elif resultado is False:
                    menu_error_success("Nenhum usuário encontrado com esse ID.")
                else:
                    menu_error_success("Erro ao deletar usuário")
                
                call_to_action_clear()
                break


def menu_remover_usuários():
    while True:
        clear()
        render_menu_remover_usuario()
        escolha = input("> ").strip()
        match escolha:
            case "1":
                remover_usuario(1, "aluno")
            case "2":
                remover_usuario(2, "professor")
            case "3":
                remover_usuario(3, "coordenador")
            case "4":
                return
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()
                continue


def rodar_menu():
    while True:
        clear()
        render_menu_coordenador()
        escolha = input("> ").strip()

        match escolha:
            case "1":
                clear()
                menu_cadastrar_usuarios()
            case "2":
                clear()
                menu_visualizar_usuarios()
            case "3":
                clear()
                menu_remover_usuários()
            case "4":
                menu_error_success("Serviço encerrado...")
                break
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()
