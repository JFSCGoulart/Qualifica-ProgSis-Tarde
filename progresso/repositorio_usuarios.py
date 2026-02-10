import sqlite3
from sqlite3 import IntegrityError

from progresso.modelos import password_hash

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()


def inserir_usuario(usuario) -> int | str | None:
    try:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, cpf, tipo, senha)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario.nome, usuario.email, usuario.cpf, usuario.tipo, usuario.senha_hash),
        )
        conexao.commit()
        return cursor.lastrowid

    except IntegrityError:
        return "cpf_ou_email_ja_cadastrado"
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None


def buscar_usuario_por_email(email: str):
    cursor.execute(
        """
        SELECT id_usuario, nome, email, cpf, tipo, senha
        FROM usuarios
        WHERE email = ?
        """,
        (email,),
    )
    return cursor.fetchone()


def buscar_usuario_por_cpf(cpf: str):
    cursor.execute(
        """
        SELECT id_usuario, nome, email, cpf, tipo, senha
        FROM usuarios
        WHERE cpf = ?
        """,
        (cpf,),
    )
    return cursor.fetchone()


def buscar_usuario_por_id(user_id: int):
    cursor.execute(
        """
        SELECT id_usuario, nome, email, cpf, tipo, senha
        FROM usuarios
        WHERE id_usuario = ?
        """,
        (user_id,),
    )
    return cursor.fetchone()


def buscar_usuario_por_tipo(tipo_num: int):
    cursor.execute(
        """
        SELECT id_usuario, nome, email, cpf, tipo
        FROM usuarios
        WHERE tipo = ?
        """,
        (tipo_num,),
    )
    return cursor.fetchall()


def buscar_usuario_por_id_e_tipo(user_id: int, tipo_num: int):
    cursor.execute(
        """
        SELECT id_usuario, nome, email, cpf, tipo
        FROM usuarios
        WHERE id_usuario = ? AND tipo = ?
        """,
        (user_id, tipo_num),
    )
    return cursor.fetchone()


def buscar_hash_senha_por_id_e_tipo(user_id: int, tipo_num: int):
    cursor.execute(
        """
        SELECT senha
        FROM usuarios
        WHERE id_usuario = ? AND tipo = ?
        """,
        (user_id, tipo_num),
    )
    linha = cursor.fetchone()
    return linha[0] if linha else None


def atualizar_nome(user_id: int, novo_nome: str, tipo_num: int) -> str:
    usuario = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
    if not usuario:
        return "nao_encontrado"

    _id, nome_atual, _email, _cpf, _tipo = usuario

    if novo_nome == nome_atual:
        return "sem_alteracao"

    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET nome = ?
            WHERE id_usuario = ? AND tipo = ?
            """,
            (novo_nome, user_id, tipo_num),
        )
        conexao.commit()
        return "atualizado"
    except Exception:
        return "erro"

def atualizar_email(user_id: int, novo_email: str, tipo_num: int) -> str:
    # 1) Verifica se o usuário existe e pega o email atual
    usuario = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
    if not usuario:
        return "nao_encontrado"

    _id, _nome, email_atual, _cpf, _tipo = usuario

    # 2) Verifica se houve mudança
    if novo_email == email_atual:
        return "sem_alteracao"

    # 3) Tenta atualizar (pode bater UNIQUE)
    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET email = ?
            WHERE id_usuario = ? AND tipo = ?
            """,
            (novo_email, user_id, tipo_num),
        )
        conexao.commit()
        return "atualizado"

    except IntegrityError:
        # outro usuário já tem esse email
        return "email_ja_cadastrado"

    except Exception:
        return "erro"


def atualizar_cpf(user_id: int, novo_cpf: str, tipo_num: int) -> str:
    # 1) Verifica se o usuário existe e pega o cpf atual
    usuario = buscar_usuario_por_id_e_tipo(user_id, tipo_num)
    if not usuario:
        return "nao_encontrado"

    _id, _nome, _email, cpf_atual, _tipo = usuario

    # 2) Verifica se houve mudança
    if novo_cpf == cpf_atual:
        return "sem_alteracao"

    # 3) Tenta atualizar (pode bater UNIQUE)
    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET cpf = ?
            WHERE id_usuario = ? AND tipo = ?
            """,
            (novo_cpf, user_id, tipo_num),
        )
        conexao.commit()
        return "atualizado"

    except IntegrityError:
        # outro usuário já tem esse cpf
        return "cpf_ja_cadastrado"

    except Exception:
        return "erro"


def atualizar_senha(user_id: int, tipo_num: int, senha_atual: str, nova_senha: str, confirmacao: str) -> str:
    senha_hash_atual = buscar_hash_senha_por_id_e_tipo(user_id, tipo_num)
    if not senha_hash_atual:
        return "nao_encontrado"

    if nova_senha != confirmacao:
        return "senhas_nao_coincidem"

    verified, _new_hash = password_hash.verify_and_update(senha_atual, senha_hash_atual)
    if not verified:
        return "senha_atual_incorreta"

    novo_hash = password_hash.hash(nova_senha)

    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET senha = ?
            WHERE id_usuario = ? AND tipo = ?
            """,
            (novo_hash, user_id, tipo_num),
        )
        conexao.commit()
        return "atualizado"
    except Exception:
        return "erro"

def atualizar_hash(user_id: int, novo_hash: str) -> str:
    cursor.execute(
        "UPDATE usuarios SET senha = ? WHERE id_usuario = ?",
        (novo_hash, user_id),
    )
    conexao.commit()
    if cursor.rowcount == 1:
        return "atualizado"
    return "nao_encontrado"


def atualizar_tipo(user_id: int, novo_tipo: str, tipo_num: int) -> str:
    cursor.execute(
        """
        UPDATE usuarios SET tipo = ?
        WHERE id_usuario = ? AND tipo = ?
        """,
        (novo_tipo, user_id, tipo_num),
    )
    conexao.commit()
    if cursor.rowcount == 1:
        return "atualizado"
    return "nao_encontrado"


def usuario_tem_vinculos(user_id: int) -> bool:
    cursor.execute(
        "SELECT 1 FROM usuario_curso WHERE id_usuario = ? LIMIT 1",
        (user_id,),
    )
    if cursor.fetchone():
        return True

    cursor.execute(
        "SELECT 1 FROM usuario_atividade WHERE id_usuario = ? LIMIT 1",
        (user_id,),
    )
    return cursor.fetchone() is not None


def deletar_usuario(user_id: int, tipo_num: int) -> str:
    if usuario_tem_vinculos(user_id):
        return "possui_vinculos"

    try:
        cursor.execute(
            "DELETE FROM usuarios WHERE id_usuario = ? AND tipo = ?",
            (user_id, tipo_num),
        )
        conexao.commit()

        if cursor.rowcount == 1:
            return "deletado"
        return "nao_encontrado"

    except IntegrityError:
        return "possui_vinculos"
    except Exception:
        return "erro"
