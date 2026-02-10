import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()


def existem_atividade_no_curso(nome_curso) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM usuario_atividade ua
        JOIN atividades a
            ON a.id_atividade = ua.id_atividade
        JOIN cursos c
            ON c.id_curso = a.id_curso
        WHERE c.nome = ?
        LIMIT 1;
        """,
        (nome_curso,)
    )

    return cursor.fetchone() is not None


def ranquear_alunos(nome_curso):
    cursor.execute(
        """
        SELECT
            usuarios.nome AS nome_usuario,
            COUNT(usuario_atividade.id_atividade) AS quantidade_atividades_feitas,
            COALESCE(
                SUM(
                    CASE
                        WHEN usuario_atividade.status = 1 THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS quantidade_atividades_acertadas
        FROM cursos
        JOIN usuario_curso
            ON usuario_curso.id_curso = cursos.id_curso
        JOIN usuarios
            ON usuarios.id_usuario = usuario_curso.id_usuario
        LEFT JOIN atividades
            ON atividades.id_curso = cursos.id_curso
        LEFT JOIN usuario_atividade
            ON usuario_atividade.id_usuario = usuarios.id_usuario
           AND usuario_atividade.id_atividade = atividades.id_atividade
        WHERE cursos.nome = ?
        GROUP BY
            usuarios.id_usuario
        ORDER BY
            quantidade_atividades_acertadas DESC,
            usuarios.nome;
        """,
        (nome_curso,)
    )
    return cursor.fetchall()


def total_atividades_hoje(nome_curso):
    cursor.execute(
        """
        SELECT
            COUNT(DISTINCT usuario_atividade.id_usuario) AS quantidade_de_alunos,
            COUNT(usuario_atividade.id_atividade) AS quantidade_atividades_feitas,
            MAX(usuario_atividade.data) AS ultima_data_registrada
        FROM usuario_atividade
        JOIN atividades
            ON atividades.id_atividade = usuario_atividade.id_atividade
        JOIN cursos
            ON cursos.id_curso = atividades.id_curso
        WHERE cursos.nome = ?
          AND usuario_atividade.data = DATE('now', 'localtime');
        """,
        (nome_curso,)
    )
    return cursor.fetchone()


def desempenho_por_curso(nome_curso):
    cursor.execute(
        """
        SELECT
            COUNT(DISTINCT usuarios.id_usuario) AS quant_matriculados,
            COUNT(DISTINCT atividades.id_atividade) AS quant_questoes,
            COUNT(DISTINCT usuario_atividade.id_usuario) AS quant_fizeram,
            COALESCE(
                SUM(
                    CASE
                        WHEN usuario_atividade.status = 1 THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS total_acertos
        FROM cursos
        LEFT JOIN usuario_curso
            ON usuario_curso.id_curso = cursos.id_curso
        LEFT JOIN usuarios
            ON usuarios.id_usuario = usuario_curso.id_usuario
        LEFT JOIN atividades
            ON atividades.id_curso = cursos.id_curso
        LEFT JOIN usuario_atividade
            ON usuario_atividade.id_usuario = usuarios.id_usuario
           AND usuario_atividade.id_atividade = atividades.id_atividade
        WHERE cursos.nome = ?;
        """,
        (nome_curso,)
    )
    return cursor.fetchone()
