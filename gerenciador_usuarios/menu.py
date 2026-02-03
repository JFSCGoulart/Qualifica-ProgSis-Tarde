from cadrasto_classes import *
from getpass import getpass
import re

listar_professor = []
listar_aluno = []
listar_coordenador = []

def formatar_cpf(cpf: str) -> str | None:
       numeros = re.sub(r"\D", "", cpf)

       if len(numeros) != 11:
              return None
       
       return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

def perguntar(prompt: str, secret = False):
       while True:
            value = getpass(prompt) if secret else input(prompt)
            value = value.strip()
            
            if value == "<":
                   return None
            if value == "":
                   print("Não pode ficar vazio. Digite novamente ou '<' pra voltar.")
                   continue
            return value

def cadastrar_professor():
    while True:
        print("Tenha em mãos nome, CPF, email e curso")

        nome = perguntar("Adicione o nome completo do(a) professor(a) (ou '<' pra voltar): ")
        if nome is None:
               break

        email = perguntar(f"Adicione o email do(a) professor(a) {nome} (ou '<' pra voltar): ")
        if email is None:
               break
        
        while True:
            cpf_raw = perguntar(
                f"Adicione o CPF do(a) professor(a) {nome} (somente números ou XXX.XXX.XXX-XX). "
                "Digite '<' pra voltar: "
            )
            if cpf_raw is None:
                return
            
            cpf_formatado = formatar_cpf(cpf_raw)
            if cpf_formatado is None:
                print("CPF inválido. Tente novamente.")
                continue

            break

        while True:
            senha = perguntar("Digite a senha (ou '<' pra voltar): ", secret = True)
            if senha is None:
                return

            senha_confirmacao = perguntar("Digite a senha novamente: ", secret = True)
            if senha_confirmacao is None:
                return

            prof = Professor(nome, email, cpf_formatado, senha, senha_confirmacao)
            
            if prof.senha_hash is None:
                print("As senhas não coincidem!")
                continue

            print("Cadastro realizado com sucesso!")
            break

        stop = input("Deseja adicionar mais professores? (s/n): ").strip().lower()
        if stop != "s":
            break

def cadastrar_aluno():
    while True:
        print("Tenha em mãos nome, CPF, email e curso")

        nome = perguntar("Adicione o nome completo do aluno(a) (ou '<' pra voltar): ")
        if nome is None:
               break

        email = perguntar(f"Adicione o email do(a) aluno(a) {nome} (ou '<' pra voltar): ")
        if email is None:
               break
        
        while True:
            cpf_raw = perguntar(
                f"Adicione o CPF do(a) aluno(a) {nome} (somente números ou XXX.XXX.XXX-XX). "
                "Digite '<' pra voltar: "
            )
            if cpf_raw is None:
                return
            
            cpf_formatado = formatar_cpf(cpf_raw)
            if cpf_formatado is None:
                print("CPF inválido. Tente novamente.")
                continue

            break

        while True:
            senha = perguntar("Digite a senha (ou '<' pra voltar): ", secret = True)
            if senha is None:
                return

            senha_confirmacao = perguntar("Digite a senha novamente: ", secret = True)
            if senha_confirmacao is None:
                return

            prof = Professor(nome, email, cpf_formatado, senha, senha_confirmacao)
            
            if prof.senha_hash is None:
                print("As senhas não coincidem!")
                continue

            print("Cadastro realizado com sucesso!")
            break

        stop = input("Deseja adicionar mais alunos? (s/n): ").strip().lower()
        if stop != "s":
            break

def cadastrar_coordenador():
    while True:
        print("Tenha em mãos nome, CPF, email e curso")

        nome = perguntar("Adicione o nome completo do do(a) coordenador(a) (ou '<' pra voltar): ")
        if nome is None:
               break

        email = perguntar(f"Adicione o email do(a) coordenador(a) {nome} (ou '<' pra voltar): ")
        if email is None:
               break
        
        while True:
            cpf_raw = perguntar(
                f"Adicione o CPF do(a) coordenador(a) {nome} (somente números ou XXX.XXX.XXX-XX). "
                "Digite '<' pra voltar: "
            )
            if cpf_raw is None:
                return
            
            cpf_formatado = formatar_cpf(cpf_raw)
            if cpf_formatado is None:
                print("CPF inválido. Tente novamente.")
                continue

            break

        while True:
            senha = perguntar("Digite a senha (ou '<' pra voltar): ", secret = True)
            if senha is None:
                return

            senha_confirmacao = perguntar("Digite a senha novamente: ", secret = True)
            if senha_confirmacao is None:
                return

            prof = Professor(nome, email, cpf_formatado, senha, senha_confirmacao)
            
            if prof.senha_hash is None:
                print("As senhas não coincidem!")
                continue

            print("Cadastro realizado com sucesso!")
            break

        stop = input("Deseja adicionar mais coordenadores? (s/n): ").strip().lower()
        if stop != "s":
            break

def visualizar():
        print("\n === Visualizar ===")
        print("1. Lista de professores")
        print("2. Lista de alunos")
        print("3. Lista de Coordenador")
        opcao_visualizar = input("Escolha a opção desejada")

        match opcao_visualizar:
                case "1":
                        if not listar_professor:
                                print("Não há registro de professores")
                        else:
                                for prof in listar_professor:
                                        print(prof)
                case "2":
                        if not listar_aluno:
                                print("Não há registro de alunos")
                        else:
                                for alu in listar_aluno:
                                        print(alu)
                case "3":
                        if not listar_coordenador:
                                print("Não há registro de coordenador")
                        else:
                                for coo in listar_coordenador:
                                        print(coo)
                case _:
                        print("opção invalida")

def rodar_menu():
        while True:
                print("Gerenciamento de usuários" )
                print("1- Cadastrar um novo professor")
                print("2- Cadastrar um novo aluno")
                print("3- Cadastrar um novo coordenador")
                print("4- Vizualizar a lista de professores, alunos ou c")
                #print("- Retirar do sistema professor ou aluno")
                print("5- sair")
                opcao_desejada = input("Escolha a opção desejada")
                match opcao_desejada:
                    case "1":
                                cadastrar_professor()
                    case "2":
                                cadastrar_aluno()
                    case "3":
                              cadastrar_coordenador()
                    case "4":
                                visualizar()
                    # case "4":
                    #             retirar()
                    case "5":
                                print("serviço encerrado")
                                break
                    case _:
                                print("opção invalida")
