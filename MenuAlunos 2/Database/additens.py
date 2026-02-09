import sqlite3

conexao = sqlite3.connect('Database/cursos.db')
cursor = conexao.cursor()

# cursor.execute(
#     "INSERT INTO cursos (nome) VALUES (?)",
#     ("Banco de dados",)
# )

# cursor.execute(
#      "INSERT INTO atividades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
#      (2, "Qual destes é um banco de dados?", "HTML", "Python", "SQL", "CSS3", "C", "Query", 1)
#  )

# cursor.execute("""
#       ALTER TABLE atividades
#        ADD COLUMN ativo_ranking DEFAULT 1
#    """)
# conexao.commit()

# cursor.execute(
#        "INSERT INTO matriculas (id_aluno, id_curso) VALUES (?, ?)",
#        (14, 2)
#    )

# cursor.execute("""
#     UPDATE progresso
#     SET nome_aluno = ?
#     WHERE id_aluno = ?
# """, ("Alessandro", 12))

# cursor.execute("""
#      UPDATE atividades 
#       SET feito = 1
#      WHERE id_curso = 2
#      """)

# cursor.execute("DROP TABLE IF EXISTS progressoAtividade")

# cursor.execute(
#         "INSERT INTO matriculas (id_aluno, id_curso) VALUES (?, ?)",
#         (14, 2)
#    )

#cursor.execute("DELETE FROM progresso WHERE id_aluno = 14 AND id_curso = 2")


usuarios = [
     ('Ana Silva', 'ana@email.com', 123456789, 'senha123', 1),
     ('Bruno Souza', 'bruno@email.com', 987654321, 'senha456', 1),
     ('Carla Dias', 'carla@email.com', 456789123, 'senha789', 2)
 ]

cursor.executemany('''
     INSERT INTO usuarios (nome, email, cpf, senha, tipo) 
     VALUES (?, ?, ?, ?, ?)
 ''', usuarios)


cursos = [
     ('Python para Iniciantes', 40),
     ('Banco de Dados SQL', 30),
     ('Desenvolvimento Web', 60)
 ]

cursor.executemany('''
     INSERT INTO cursos (nome, horario) 
     VALUES (?, ?)
 ''', cursos)



atividades = [
      
     ('Qual o comando para imprimir no console?', 'print()', 'input()', 'echo', 'log', 'A', 'É uma função nativa do Python.', 1),
     ('Como se declara uma lista em Python?', '()', '{}', '[]', '<>', 'C', 'Lembre-se dos colchetes.', 1),
    
      
     ('Qual comando deleta todos os dados de uma tabela?', 'REMOVE', 'DELETE', 'DROP', 'TRUNCATE', 'B', 'Pode ser usado com WHERE.', 2),
    
      
     ('O que significa HTML?', 'HyperText Markup Language', 'High Tech Modern Language', 'Hyperlink Text Management', 'Home Tool Markup', 'A', 'É uma linguagem de marcação.', 3)
 ]

cursor.executemany('''
     INSERT INTO atividades (questao, A, B, C, D, gabarito, dica, id_curso) 
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
 ''', atividades)

matriculas = [
     (1, 1),  
     (1, 2),  
     (2, 1),  
     (3, 3)  
 ]

cursor.executemany('''
     INSERT INTO usuario_curso (id_usuario, id_curso) 
     VALUES (?, ?)
 ''', matriculas)

conexao.commit()
print("Adicionado com sucesso!")
conexao.close()