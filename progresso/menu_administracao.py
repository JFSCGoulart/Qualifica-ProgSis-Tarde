from progresso.modelos import Aluno, Coordenador, Professor

from progresso.repositorio_usuario import (
    buscar_usuario_por_id_e_tipo,
    buscar_usuario_por_tipo,
    buscar_usuario_por_email,
    buscar_usuario_por_cpf,
    deletar_usuario,
    inserir_usuario,
)

from progresso.validadores import formatar_cpf, validar_email
from progresso.prompts import perguntar

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


def tratar_retorno_atualizacao(status: str, campo: str):
    match status:
        case "atualizado":
            menu_feedback(f"{campo} atualizado com sucesso!")
        case "nao_encontrado":
            menu_feedback("Usuário não encontrado.")
        case "sem_alteracao":
            menu_feedback(f"Nenhuma alteração: {campo} informado é igual ao atual.")
        case "email_ja_cadastrado":
            menu_feedback("Email já cadastrado.")
        case "cpf_ja_cadastrado":
            menu_feedback("CPF já cadastrado.")
        case "senhas_nao_coincidem":
            menu_feedback("As senhas não coincidem.")
        case "senha_atual_incorreta":
            menu_feedback("Senha atual incorreta.")
        case "tipo_invalido":
            menu_feedback("Tipo inválido.")
        case "erro":
            menu_feedback("Erro ao atualizar.")
        case _:
            menu_feedback("Resposta inesperada do sistema.")


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
            
            verificar_email = buscar_usuario_por_email(email)
                
            if verificar_email:
                menu_feedback("Email já cadastrado.")
                call_to_action_clear()
                continue

            if not validar_email(email):
                menu_feedback("Email inválido. Tente novamente.")
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
                menu_feedback("CPF inválido. Tente novamente.")
                call_to_action_clear()
                continue

            verificar_cpf = buscar_usuario_por_cpf(cpf_formatado)
                
            if verificar_cpf:
                menu_feedback("CPF já cadastrado.")
                call_to_action_clear()
                continue

            step = "senha"

        elif step == "senha":
            senha = senha_confirmacao = (nome[:3]) + "@" + (str(cpf_raw)[-4:])

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
                menu_feedback(str(e))
                call_to_action_clear()
                continue

            resultado = inserir_usuario(novo_user)

            if isinstance(resultado, int):
                id_usuario_novo = resultado
                clear()
                menu_feedback("Cadastro realizado com sucesso!")

            if tipo_num == 1:
                cursos = listar_cursos()

                if not cursos:
                    menu_feedback("Nenhum curso cadastrado. Aluno foi criado sem matrícula.")
                else:
                    while True:
                        print("\nSelecione um curso para matricular o aluno (ou '<' para pular):\n")

                        for i, (_id_curso, nome_curso, horario) in enumerate(cursos, start=1):
                            print(f"{i}. {nome_curso} (horário: {horario})")

                        escolha = input("\n> ").strip()

                        if escolha == "<":
                            menu_feedback("Aluno criado sem matrícula.")
                            break

                        if not escolha.isdigit():
                            menu_feedback("Opção inválida. Digite um número da lista ou '<'.")
                            continue

                        idx = int(escolha)
                        if idx < 1 or idx > len(cursos):
                            menu_feedback("Opção fora da lista. Tente novamente.")
                            continue

                        id_curso_escolhido = cursos[idx - 1][0]
                        status_matricula = matricular_usuario_em_curso(id_usuario_novo, id_curso_escolhido)

                        if status_matricula == "matriculado":
                            menu_feedback("Aluno matriculado no curso com sucesso!")
                        elif status_matricula == "ja_matriculado":
                            menu_feedback("Esse aluno já está matriculado nesse curso.")
                        else:
                            menu_feedback("Erro ao matricular o aluno no curso.")

                        break

            elif resultado == "cpf_ou_email_ja_cadastrado":
                clear()
                menu_feedback("CPF ou email já cadastrado.")
            else:
                clear()
                menu_feedback("Erro crítico ao acessar o banco.")

            while True:
                stop = input(f"\nDeseja adicionar mais {label}s? (s/n): ").strip().lower()

                match stop:
                    case "s":
                        nome = email = cpf_formatado = None
                        step = "nome"
                        break
                    case "n":
                        return
                    case _:
                        menu_feedback("Resposta inválida. Digite 's' para sim ou 'n' para não.")
                        call_to_action_clear()
                        continue


def menu_cadastrar_usuarios():
    while True:
        clear()
        render_menu_tipo_usuario("CADASTRAR")
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
                menu_feedback("Opção inválida.")
                call_to_action_clear()
                continue


def visualizar_usuarios(tipo_num, label):
    resultado = buscar_usuario_por_tipo(tipo_num)

    if not resultado:
        menu_feedback(f"Nenhum {label.lower()} cadastrado.")
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


def selecionar_usuario_por_id(tipo_num: int, label: str):
    while True:
        clear()

        usuarios = buscar_usuario_por_tipo(tipo_num)
        if not usuarios:
            menu_feedback(f"Nenhum {label.lower()} cadastrado.")
            call_to_action_clear()
            return None

        print(f"=== Lista de {label}s ===")
        for id, nome, email, cpf, *_ in usuarios:
            print(f"ID: {id} | Nome: {nome} | Email: {email} | CPF: {cpf}")

        user_id_raw = input(
            f"\nDigite o ID do(a) {label} (ou '<' pra voltar): "
        ).strip()

        if user_id_raw == "<":
            return None

        if not user_id_raw.isdigit():
            menu_feedback("ID inválido. Digite um número.")
            call_to_action_clear()
            continue

        user_id = int(user_id_raw)

        clear()
        encontrado = visualizar_usuario(user_id, tipo_num, label)
        if not encontrado:
            menu_feedback("Nenhum usuário encontrado com esse ID.")
            call_to_action_clear()
            continue

        return user_id


def menu_visualizar_usuarios():
    while True:
        clear()
        render_menu_tipo_usuario("VISUALIZAR")
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
                menu_feedback("Opção inválida.")
                call_to_action_clear()
                continue


def editar_nome(user_id, tipo_num, render):
    while True:
        render()
        novo_nome = input("\nNovo nome (ou '<' pra voltar): ").strip()

        if novo_nome == "<":
            return

        if not novo_nome:
            menu_feedback("Nome não pode ser vazio.")
            call_to_action_clear()
            continue

        status = atualizar_nome(user_id, novo_nome, tipo_num)
        tratar_retorno_atualizacao(status, "Nome")
        call_to_action_clear()
        return


def editar_email(user_id, tipo_num, render):
    while True:
        render()
        novo_email = input("\nNovo email (ou '<' pra voltar): ").strip()

        if novo_email == "<":
            return

        novo_email = novo_email.strip().lower()

        if not validar_email(novo_email):
            menu_feedback("Email inválido.")
            call_to_action_clear()
            continue

        # Pré-checagem pra feedback melhor (opcional, mas útil)
        ja_existe = buscar_usuario_por_email(novo_email)
        if ja_existe and ja_existe[0] != user_id:
            tratar_retorno_atualizacao("email_ja_cadastrado", "Email")
            call_to_action_clear()
            continue

        status = atualizar_email(user_id, novo_email, tipo_num)
        tratar_retorno_atualizacao(status, "Email")
        call_to_action_clear()
        return


def editar_cpf(user_id, tipo_num, render):
    while True:
        render()
        novo_cpf_raw = input("\nNovo CPF (ou '<' pra voltar): ").strip()

        if novo_cpf_raw == "<":
            return

        novo_cpf = formatar_cpf(novo_cpf_raw)
        if novo_cpf is None:
            menu_feedback("CPF inválido.")
            call_to_action_clear()
            continue

        ja_existe = buscar_usuario_por_cpf(novo_cpf)
        if ja_existe and ja_existe[0] != user_id:
            tratar_retorno_atualizacao("cpf_ja_cadastrado", "CPF")
            call_to_action_clear()
            continue

        status = atualizar_cpf(user_id, novo_cpf, tipo_num)
        tratar_retorno_atualizacao(status, "CPF")
        call_to_action_clear()
        return


def editar_senha(user_id, render):
    while True:
        render()
        nova_senha = input("\nNova senha (ou '<' pra voltar): ").strip()
        if nova_senha == "<":
            return

        if not nova_senha:
            menu_feedback("A nova senha não pode ser vazia.")
            call_to_action_clear()
            continue

        confirmacao = input("\nConfirme a nova senha: ").strip()

        if nova_senha != confirmacao:
            tratar_retorno_atualizacao("senhas_nao_coincidem", "Senha")
            call_to_action_clear()
            continue

        novo_hash = password_hash.hash(nova_senha)

        status = atualizar_hash(user_id, novo_hash)
        tratar_retorno_atualizacao(status, "Senha")
        call_to_action_clear()
        return


def editar_tipo(user_id, tipo_num, label, render):
    while True:
        render()
        render_menu_novo_tipo_usuario()
        novo_tipo_raw = input("> ").strip()

        match novo_tipo_raw:
            case "1":
                novo_tipo = 1
            case "2":
                novo_tipo = 2
            case "3":
                novo_tipo = 3
            case "4":
                return tipo_num, label  # volta ao menu anterior
            case _:
                menu_feedback("Opção inválida.")
                call_to_action_clear()
                continue

        if novo_tipo == tipo_num:
            tratar_retorno_atualizacao("sem_alteracao", "Tipo")
            call_to_action_clear()
            continue

        status = atualizar_tipo(user_id, novo_tipo, tipo_num)
        tratar_retorno_atualizacao(status, "Tipo")
        call_to_action_clear()

        if status == "atualizado":
            tipo_num = novo_tipo
            match tipo_num:
                case 1:
                    label = "aluno"
                case 2:
                    label = "professor"
                case 3:
                    label = "coordenador"

            return tipo_num, label


def editar_usuario(tipo_num, label):
    user_id = selecionar_usuario_por_id(tipo_num, label)
    if user_id is None:
        return

    while True:
        clear()

        usuario = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
        if not usuario:
            menu_feedback("Usuário não encontrado.")
            call_to_action_clear()
            return

        render_usuario_em_edicao(user_id, label, usuario)

        render_menu_editar_usuario()
        escolha = input("> ").strip()

        match escolha:
            case "1":
                def render():
                    clear()
                    usuario_atual = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
                    render_usuario_em_edicao(user_id, label, usuario_atual)

                editar_nome(user_id, tipo_num, render)

            case "2":
                def render():
                    clear()
                    usuario_atual = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
                    render_usuario_em_edicao(user_id, label, usuario_atual)

                editar_email(user_id, tipo_num, render)

            case "3":
                def render():
                    clear()
                    usuario_atual = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
                    render_usuario_em_edicao(user_id, label, usuario_atual)

                editar_cpf(user_id, tipo_num, render)

            case "4":
                def render():
                    clear()
                    usuario_atual = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
                    render_usuario_em_edicao(user_id, label, usuario_atual)

                editar_senha(user_id, render)

            case "5":
                def render():
                    clear()
                    usuario_atual = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
                    render_usuario_em_edicao(user_id, label, usuario_atual)

                tipo_num, label = editar_tipo(user_id, tipo_num, label, render)

            case "6":
                return

            case _:
                menu_feedback("Opção inválida.")
                call_to_action_clear()


def menu_editar_usuario():
    while True:
        clear()
        render_menu_tipo_usuario("EDITAR")
        escolha = input("> ").strip()
        match escolha:
            case "1":
                editar_usuario(1, "aluno")
            case "2":
                editar_usuario(2, "professor")
            case "3":
                editar_usuario(3, "coordenador")
            case "4":
                return
            case _:
                menu_feedback("Opção inválida.")
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
