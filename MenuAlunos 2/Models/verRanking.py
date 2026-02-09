import sqlite3

from Connection.conexao import cursor, conexao

#busca o curso que o aluno esta matriculado
def ranking(id_usuario):
    # Busca cursos onde o aluno está matriculado
    cursor.execute("""
        SELECT cursos.id_curso, cursos.nome, cursos.horario
        FROM cursos
        INNER JOIN usuario_curso ON cursos.id_curso = usuario_curso.id_curso
        WHERE usuario_curso.id_usuario = ?
    """, (id_usuario,))
    #transforma a busca em uma variavel
    cursos = cursor.fetchall()

    #Percorre a lista e verifica se existe cursos nela
    if not cursos:
        print("\nNenhum curso encontrado para este aluno.")
        return

    print("\n--- MEUS CURSOS ---")
    #se existir esse codigo mostra o id[0] do curso e o nome[1] dele
    for curso in cursos:
        print(f"ID: {curso[0]} | Nome: {curso[1]} | Horario: {curso[2]}" )

    ids_validos = [curso[0] for curso in cursos]

    while True:
        #tratamento de erro para caso o aluno digite um ID que não existe ou outra coisa que não seja numero
        try:
            qualcurso = int(input("\nDigite o ID do curso para ver o ranking: "))
            if qualcurso in ids_validos:
                #Chama a função de ranking com o ID escolhido
                ranking_geral(qualcurso) 
                break
            else:
                print("Curso Inválido. Escolha um ID da lista acima.")
        except ValueError:
            print("Entrada inválida. Digite apenas o número do ID.")
#mostra o ranking para o aluno
def ranking_geral(id_curso):
    # Busca o ranking filtrando pelo ID do curso passado pela função anterior
    cursor.execute("""
     SELECT u.nome, COUNT(ua.acerto) AS total_acertos
     FROM usuarios u
     JOIN usuario_atividade ua on u.id_usuario = ua.id_usuario
     JOIN atividades a ON ua.id_atividade = a.id_atividades            
     WHERE ua.acerto = 1 AND a.id_curso = ?
     GROUP BY u.id_usuario, u.nome ORDER BY total_acertos DESC                                                    
""", (id_curso,))
    #transforma a busca em variavel
    ranking = cursor.fetchall()

    print(f"\n=== RANKING DO CURSO (ID: {id_curso}) ===")

    if not ranking:
        print("Ainda não há dados de progresso para este curso.")
        return
    
    #percorre a lista de alunos e organiza nas posicões
    for posicao, aluno in enumerate(ranking, start=1):
        nome_aluno, estrelas = aluno
        # Printa as posiçoes
        print(f"{posicao}º - {nome_aluno} | ⭐ {estrelas}")     

    
