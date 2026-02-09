import sqlite3

from funcoes import *
from funcoes_tarefas import *

#Função que exemplifica o menu do usuário( ilustrativo )

def stil():
    print("\n --- BEM VINDO! --- \n")
    print("O que você deseja fazer? ")
    print("1. Visualizar seus cursos")
    print("2. Adicionar um curso")
    print("3. Adicionar questões a um conteúdo")
    print("4. Ver as atividades de um curso")
    print("5. Excluir curso")
    print("6. Excluir questões")
    print("7. Sair")


#Função que lê a opção do usuário com tratamento de erro!
#(o try serve para que o usuário digite um número inteiro o menu de opções apareça)
#(e except inválida tudo que não for número).

def obter_opcao():
    
    try:
        return int(input("Digite a opção que você deseja: "))
    except ValueError:
        print("Entrada inválida. Digite apenas números.")
        return None

#Função onde executa as funções de Professor!

def execucao():
    while True:
        stil() 
        opcao = obter_opcao()

        if opcao is None:
            continue

        if opcao == 1:
            ver_materia()
        elif opcao == 2:
            adicionar_curso()
        elif opcao == 3:
            adicionar_questao()
        elif opcao == 4:
            ver_questoes()
        elif opcao == 5:
            excluir_curso()
        elif opcao == 6:
            excluir_atividade()
        elif opcao == 7:
            print("\n---- Saindo do sistema ----\n")
            break
        else:
            print("Opção inválida. Tente novamente.")



#Função principal do sistema.

def main():
    conexao = sqlite3.connect("objetos.db")
    cursor = conexao.cursor()

    try:
        execucao()
    finally:
        conexao.close()


if __name__ == "__main__":
    main()

