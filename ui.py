import os
import platform


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def menu_feedback(text):
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


def menu_subtitulo(name):
    print(f"\n{name}")


def render_menu_coordenador():
    menu_title("COORDENADOR")
    menu_subtitulo("O que você quer fazer?")
    menu_option("1", "Cadastrar novo aluno")
    menu_option("2", "Ver ranking por turma")
    menu_option("3", "Ver total de atividades de hoje")
    menu_option("4", "Ver desempenho por curso")
    menu_option("5", "Sair")


def render_menu_escolha_curso(titulo):
    menu_title(titulo)
    menu_subtitulo("Escolha o curso:")
    menu_option("1", "Matemática")
    menu_option("2", "Português")
    menu_option("3", "História")
    menu_option("4", "Geografia")
    menu_option("5", "Ciências")
    menu_option("6", "Voltar")


def render_menu_gerenciar_usuarios():
    menu_title("USUÁRIOS")
    menu_subtitulo("O que você quer fazer?")
    menu_option("1", "Cadastrar")
    menu_option("2", "Visualizar")
    menu_option("3", "Editar")
    menu_option("4", "Remover")
    menu_option("5", "Voltar")


def render_menu_tipo_usuario(operacao):
    menu_title(f"{operacao} USUÁRIO")
    menu_subtitulo("Escolha uma opção:")
    menu_option("1", "Aluno")
    menu_option("2", "Professor")
    menu_option("3", "Coordenador")
    menu_option("4", "Voltar")

def render_menu_novo_tipo_usuario():
    menu_subtitulo("Escolha o novo tipo de usuário:")
    menu_option("1", "Aluno")
    menu_option("2", "Professor")
    menu_option("3", "Coordenador")
    menu_option("4", "Voltar")

def render_usuario_em_edicao(user_id, label, usuario):
    _id, nome, email, cpf, tipo = usuario

    menu_title("EDITAR USUÁRIO")
    print(f"\nID: {user_id} | Tipo: {label}")
    print(f"Nome: {nome}")
    print(f"Email: {email}")
    print(f"CPF: {cpf}")

def render_menu_editar_usuario():
    menu_subtitulo("O que você quer editar?")
    menu_option("1", "Nome")
    menu_option("2", "Email")
    menu_option("3", "CPF")
    menu_option("4", "Senha")
    menu_option("5", "Tipo")
    menu_option("6", "Voltar")


def render_menu_cadastrar_usuario(tipo):
    menu_title(f"CADASTRAR {tipo}")
    menu_subtitulo(
        "Antes de começar, tenha em mãos o nome completo, CPF e e-mail do usuário."
    )
