import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()


def listar_cursos():
    cursor.execute(
        """
        SELECT id_curso, nome, horario
        FROM cursos
        ORDER BY nome;
        """
    )
    return cursor.fetchall()

def matricular_usuario_em_curso(id_usuario: int, id_curso: int) -> str:
    try:
        cursor.execute(
            """
            INSERT INTO usuario_curso (id_usuario, id_curso)
            VALUES (?, ?)
            """,
            (id_usuario, id_curso),
        )
        conexao.commit()
        return "matriculado"
    except sqlite3.IntegrityError:
        # se você criar UNIQUE/PK composto, cai aqui quando tentar duplicar
        return "ja_matriculado"
    except Exception:
        return "erro"
