from cadrasto_classes import Professor, Aluno, Coordenador

listar_professor = []
listar_aluno = []
listar_coordenador = []

def cadastrar_professor():
    while True:
        curso = []
        print("Tenha em mãos nome, CPF, email e curso")

        nome = input("Adicione o nome completo do professor: ")
        cpf = input(f"Adicione o CPF do professor(a) {nome}: ")
        email = input(f"Adicione o email do professor(a) {nome}: ")

        while True:
            item = input(
                f"Adicione o curso ou cursos que o(a) professor(a) {nome} ministrará "
                "(0 para sair): "
            )
            if item == "0":
                break
            if item not in curso:
                curso.append(item)
            else:
                print("Curso já adicionado")

        prof = Professor(nome, cpf, email, curso)  
        listar_professor.append(prof)

        stop = input("Deseja adicionar mais professores? (s/n): ").lower()
        if stop != "s":
            break


def cadastrar_aluno():
    while True:
        curso = []
        print("Tenha em mãos nome, CPF, email e curso")

        nome = input("Adicione o nome completo do(a) aluno(a): ")
        cpf = input(f"Adicione o CPF do(a) aluno(a) {nome}: ")
        email = input(f"Adicione o email do(a) aluno(a) {nome}: ")

        while True:
            item = input(
                f"Adicione o curso ou cursos que o(a) aluno(a) {nome} participará "
                "(0 para sair): "
            )
            if item == "0":
                break
            if item not in curso:
                curso.append(item)
            else:
                print("Curso já adicionado")

        alu = Aluno(nome, cpf, email, curso)  
        listar_aluno.append(alu)

        stop = input("Deseja adicionar mais alunos? (s/n): ").lower()
        if stop != "s":
            break
def cadastrar_coordenador():
    while True:
        print("Tenha em mãos nome, CPF, email e curso")

        nome = input("Adicione o nome completo do(a) coordenador(a): ")
        cpf = input(f"Adicione o CPF do(a) coordenador(a) {nome}: ")
        email = input(f"Adicione o email do(a) coordenador(a) {nome}: ")
        coo = Coordenador(nome, cpf, email)  
        listar_coordenador.append(coo)

        stop = input("Deseja adicionar mais coordenadores? (s/n): ").lower()
        if stop != "s":
            break
def visualizar():
        print("\n === Visualizar ===")
        print("1. Lista de professores")
        print("2. Lista de alunos")
        print("3. Lista de Coordenador")
        #print("3. Lista de cursos")
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