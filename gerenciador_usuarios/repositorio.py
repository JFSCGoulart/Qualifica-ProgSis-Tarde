from banco import conexao, cursor
from sqlite3 import IntegrityError


def inserir_usuario(usuario) -> bool | None:
    try:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, cpf, tipo, senha)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario.nome, usuario.email, usuario.cpf, usuario.tipo, usuario.senha_hash),
        )
        conexao.commit()
        return True
    except IntegrityError:
        return False
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


def deletar_usuario(user_id: int) -> str:
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (user_id,))
    conexao.commit()
    return "deletado" if cursor.rowcount == 1 else "nao_encontrado"


def atualizar_hash(user_id: int, novo_hash: str) -> str:
    cursor.execute(
        "UPDATE usuarios SET senha = ? WHERE id_usuario = ?",
        (novo_hash, user_id),
    )
    conexao.commit()
    if cursor.rowcount == 1:
        return "atualizado"
    return "nao_encontrado"
