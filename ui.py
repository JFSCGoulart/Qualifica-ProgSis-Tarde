import os
import platform


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def menu_error_success(text):
    print(f"\n{text}")


def call_to_action_clear():
    input("\nPressione Enter para continuar...")
    clear()


def menu_title(title, width=80):
    line = "#" * width
    print(f"\n{line}")
    print(title)
    print(line)


def menu_option(number, name):
    print(f"{number}. {name}")


def single_option(name):
    print(f"\n{name}")


def render_menu_coordenador():
    menu_title("GERENCIAMENTO DE USUÁRIOS")
    single_option("Escolha uma opção:")
    menu_option("1", "Cadastrar novo usuário")
    menu_option("2", "Visualizar usuários")
    menu_option("3", "Remover usuário")
    menu_option("4", "Sair")


def render_menu_tipo_usuario():
    menu_title("SELECIONAR TIPO DE USUÁRIO")
    single_option("Selecione o tipo de usuário:")
    menu_option("1", "Aluno")
    menu_option("2", "Professor")
    menu_option("3", "Coordenador")
    menu_option("4", "Voltar")


def render_menu_cadastrar_usuario(tipo):
    menu_title(f"CADASTRAR {tipo}")
    single_option(
        "Antes de começar, tenha em mãos o nome completo, CPF e e-mail do usuário."
    )


def render_menu_visualizar_usuario():
    menu_title("VISUALIZAR USUÁRIO")
    single_option("Escolha uma opção:")
    menu_option("1", "Lista de alunos")
    menu_option("2", "Lista de professores")
    menu_option("3", "Lista de coordenadores")
    menu_option("4", "Voltar")


def render_menu_deletar_usuario():
    menu_title("DELETAR USUÁRIO")
    single_option("Escolha uma opção:")
    menu_option("1", "Alunos")
    menu_option("2", "Professores")
    menu_option("3", "Coordenadores")
    menu_option("4", "Voltar")
