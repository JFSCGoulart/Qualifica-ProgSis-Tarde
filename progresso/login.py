from getpass import getpass

from progresso.repositorio import (
    buscar_usuario_por_email,
    buscar_usuario_por_cpf,
    atualizar_hash,
)
from progresso.modelos import Usuario
from progresso.validadores import formatar_cpf


def autenticar(identificador: str, senha_digitada: str):
    identificador = identificador.strip()

    if not identificador or not senha_digitada:
        return None

    # Decide se vai buscar por email ou cpf
    if "@" in identificador:
        row = buscar_usuario_por_email(identificador.lower())
    else:
        cpf_formatado = formatar_cpf(identificador)
        if cpf_formatado is None:
            return None
        row = buscar_usuario_por_cpf(cpf_formatado)

    if row is None:
        return None

    user_id = row[0]
    senha_hash_db = row[5]

    usuario = Usuario(senha_hash_db)

    if not usuario.verificar_senha(senha_digitada):
        return None

    # Se pwdlib sugerir rehash, salva o novo hash no banco
    if usuario.senha_hash != senha_hash_db:
        atualizar_hash(user_id, usuario.senha_hash)

    return row


def rodar_login_cli():
    identificador = input("Email ou CPF: ").strip()
    senha_digitada = getpass("Senha: ").strip()

    row = autenticar(identificador, senha_digitada)

    if row is None:
        print("Credenciais inválidas.")
        return

    print("Logado!")
