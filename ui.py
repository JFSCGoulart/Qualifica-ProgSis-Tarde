import os
import platform

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def call_to_action_clear():
    input("\nPressione Enter para continuar...")
    clear()

def menu_title(title):
    print(f"\n{80 * "#"}")
    print(title)
    print(80 * "#")

def menu_option(number, name):
   print(f"{number}. {name}")

def single_option(name):
    print(f"\n{name}")

def render_menu_tipo_usuario():
    menu_title("CADASTRAR USUÁRIO")
    single_option("Selecione o tipo de usuário:")
    menu_option("1", "Professor")
    menu_option("2", "Aluno")
    menu_option("3", "Coordenador")
    menu_option("4", "Voltar")

def render_menu_coordenador():
    menu_title("GERENCIAMENTO DE USUÁRIOS")
    single_option("Escolha uma opção:")
    menu_option("1", "Cadastrar novo usuário")
    menu_option("2", "Visualizar usuários")
    menu_option("3", "Remover usuário")
    menu_option("4", "Sair")
