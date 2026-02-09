import sqlite3
from Models.ListarCursos import listar_cursos_progresso
#Importando a biblioteca das datas
from datetime import date
#conectando o banco de dados
from Connection.conexao import cursor, conexao

#Mostra o progresso do aluno no dia de hoje
def progresso_diario(id_usuario):
    
    hoje = date.today()
    # O SQL busca o total de linhas (COUNT) e a soma de acertos (SUM)
    # DATE('now') é uma função do SQLite que pega a data de hoje automaticamente
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuario_atividade
        WHERE id_usuario = ?
        AND data = ?
        AND status = 1
    """, (id_usuario, hoje))
    #Essa linha pega o resultado da conta feita pelo banco de dados (como o total de acertos) 
    # e guarda esse valor dentro de variáveis para que o Python possa usá-las.
    feitas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM usuario_atividade
        WHERE id_usuario = ?
        AND data = ?
        AND acerto = 1
    """, (id_usuario, hoje))

    acertos = cursor.fetchone()[0]

    # O uso do 'or 0' serve para evitar que apareça "None" caso o aluno não tenha feito nada hoje
    print("\n📅 PROGRESSO DE HOJE")
    print(f"Atividades feitas: {feitas or 0}")
    print(f"Estrelas Ganhas: {acertos or 0}")

#Mostra o progresso do aluno em um curso especifico
def progresso_por_curso(id_usuario):
    id_curso = listar_cursos_progresso(id_usuario)

    if not id_curso:
        return
    
    # total de atividades do curso
    cursor.execute("""
        SELECT COUNT(*)
        FROM atividades
        WHERE id_curso = ?
    """, (id_curso,))
    total = cursor.fetchone()[0]

    # feitas pelo aluno nesse curso
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuario_atividade ua
        JOIN atividades a ON ua.id_atividade = a.id_atividades
        WHERE ua.id_usuario = ?
        AND a.id_curso = ?
        AND ua.status = 1
    """, (id_usuario, id_curso))
    feitas = cursor.fetchone()[0]

    # estrelas (acertos)
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuario_atividade ua
        JOIN atividades a ON ua.id_atividade = a.id_atividades
        WHERE ua.id_usuario = ?
        AND a.id_curso = ?
        AND ua.acerto = 1
    """, (id_usuario, id_curso))
    estrelas = cursor.fetchone()[0]


    print("\n====== PROGRESSO DO CURSO ======")
    print(f"Atividades feitas: {feitas}/{total}")
    print(f"⭐ Estrelas: {estrelas}")

   
#Mostra o progresso de todos os cursos somados do alunos 
def progresso_total(id_usuario):

    # total de atividades existentes
    cursor.execute("SELECT COUNT(*) FROM atividades")
    total_atividades = cursor.fetchone()[0]

    # total feitas pelo aluno
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuario_atividade
        WHERE id_usuario = ?
        AND status = 1
    """, (id_usuario,))
    feitas = cursor.fetchone()[0]

    # total de acertos (estrelas)
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuario_atividade
        WHERE id_usuario = ?
        AND acerto = 1
    """, (id_usuario,))
    estrelas = cursor.fetchone()[0]

    print("\n====== PROGRESSO TOTAL ======")
    print(f"Atividades feitas: {feitas}/{total_atividades}")
    print(f"⭐ Estrelas: {estrelas}")
     
    