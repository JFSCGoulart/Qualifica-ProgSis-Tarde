from gerenciador_usuarios.modelos import Aluno, Professor, Coordenador
from gerenciador_usuarios.repositorio import inserir_usuario, buscar_usuario_por_tipo
from gerenciador_usuarios.validadores import formatar_cpf, validar_email
from gerenciador_usuarios.prompts import perguntar
from ui import (
    clear,
    call_to_action_clear,
    menu_error_success,
    render_menu_coordenador,
    render_menu_tipo_usuario,
    render_menu_cadastrar_usuario,
    render_menu_visualizar_usuario,
    render_menu_deletar_usuario,
)

TIPOS_USUARIO = {
    1: "Aluno",
    2: "Professor",
    3: "Coordenador",
}


def cadastrar_usuario(tipo_cls, tipo_num, label):
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
                redraw=render,
            )
            if nome is None:
                return
            step = "email"

        elif step == "email":
            email = perguntar(
                f"\nEmail do {label} {nome} (ou '<' pra voltar): ",
                redraw=render,
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
                redraw=render,
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
                secret=True,
                redraw=render,
            )
            if senha is None:
                step = "cpf"
                continue

            senha_confirmacao = perguntar(
                "\nDigite a senha novamente (ou '<' pra voltar): ",
                secret=True,
                redraw=render,
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
                    tipo=tipo_num,
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
                cadastrar_usuario(Aluno, 1, "aluno")
            case "2":
                cadastrar_usuario(Professor, 2, "professor")
            case "3":
                cadastrar_usuario(Coordenador, 3, "coordenador")
            case "4":
                break
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()


def visualizar_usuarios(tipo_num):
    tipo_texto = TIPOS_USUARIO.get(tipo_num, "Usuário")
    resultado = buscar_usuario_por_tipo(tipo_num)

    if not resultado:
        menu_error_success(f"Nenhum {tipo_texto.lower()} cadastrado.")
        return

    print(f"=== Lista de {tipo_texto}s ===")
    for user_id, nome, email, cpf, *_ in resultado:
        print(f"ID: {user_id} | Nome: {nome} | Email: {email} | CPF: {cpf}")


def funcionalidade_em_construcao(texto):
    menu_error_success(f"🚧 {texto}\nEm construção...")
    call_to_action_clear()


def menu_visualizar_usuarios():
    while True:
        clear()
        render_menu_visualizar_usuario()
        escolha = input("> ").strip()

        match escolha:
            case "1":
                clear()
                visualizar_usuarios(1)
                call_to_action_clear()
            case "2":
                clear()
                visualizar_usuarios(2)
                call_to_action_clear()
            case "3":
                clear()
                visualizar_usuarios(3)
                call_to_action_clear()
            case "4":
                break
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()


def menu_deletar():
    # ainda não conectado na regra de deletar, mas já está no padrão do UI
    while True:
        clear()
        render_menu_deletar_usuario()
        escolha = input("> ").strip()

        match escolha:
            case "1" | "2" | "3":
                funcionalidade_em_construcao("Remover usuários cadastrados")
            case "4":
                break
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()


def rodar_menu():
    while True:
        clear()
        render_menu_coordenador()
        escolha = input("> ").strip()

        match escolha:
            case "1":
                menu_cadastrar_usuarios()
            case "2":
                menu_visualizar_usuarios()
            case "3":
                funcionalidade_em_construcao("Remover usuários cadastrados")
                # ou: menu_deletar()
            case "4":
                print("\nServiço encerrado...")
                break
            case _:
                menu_error_success("Opção inválida.")
                call_to_action_clear()
