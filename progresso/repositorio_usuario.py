from banco import conexao, cursor
from sqlite3 import IntegrityError


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


def deletar_usuario(user_id: int, tipo_num: int) -> bool | None:
    cursor.execute(
        "DELETE FROM usuarios WHERE id_usuario = ? AND tipo = ?",
        (user_id, tipo_num),
    )
    conexao.commit()

    if cursor.rowcount == 1:
        return True
    return False


def atualizar_hash(user_id: int, novo_hash: str) -> str:
    cursor.execute(
        "UPDATE usuarios SET senha = ? WHERE id_usuario = ?",
        (novo_hash, user_id),
    )
    conexao.commit()
    if cursor.rowcount == 1:
        return "atualizado"
    return "nao_encontrado"
