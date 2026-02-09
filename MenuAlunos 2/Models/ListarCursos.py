#importando o banco de dados
import sqlite3
#Importando a biblioteca das datas 
from datetime import date
#importando outros codigos

# Conectando o banco de dados 
from Connection.conexao import cursor, conexao
#registra caso o usuario responda a questão errada
def registrar_resposta_errada(id_usuario, id_atividade):
    hoje = date.today()
    cursor.execute("""
            INSERT INTO usuario_atividade
            (id_usuario, id_atividade, data, acerto, status)
            VALUES (?, ?, ?, ?, ?)
        """, (id_usuario, id_atividade, hoje, 0, 1))

    conexao.commit()
    
#registra a resposta caso o usuario acertar
def registrar_resposta(id_usuario, id_atividade):
    hoje = date.today()

     #Verifica se já existe registro
    cursor.execute("""
        SELECT acerto
        FROM usuario_atividade
        WHERE id_usuario = ? AND id_atividade = ?
    """, (id_usuario, id_atividade))

    resultado = cursor.fetchone()

    if resultado is None:
        # Primeira vez = ganha estrela
        cursor.execute("""
            INSERT INTO usuario_atividade
            (id_usuario, id_atividade, data, acerto, status)
            VALUES (?, ?, ?, 1, 1)
        """, (id_usuario, id_atividade, hoje))
        conexao.commit()
        return True
    else:
        #Já fez antes → só atualiza status
        cursor.execute("""
            INSERT INTO usuario_atividade
            (id_usuario, id_atividade, data, acerto, status)
            VALUES (?, ?, ?, 0, 1)
        """, (id_usuario, id_atividade, hoje))
        conexao.commit()
        return False

#acessa a atividade do curso que o aluno escolher
def acessar_atividades(id_curso):
    cursor.execute("""
        SELECT id_atividades, questao, A, B, C, D, gabarito, dica, id_curso
        FROM atividades
        WHERE id_curso = ?
    """, (id_curso,))

    questoes = cursor.fetchall()

    if questoes:
        fazerAtividades(questoes)
    else:
        print("Nenhuma atividade encontrada.")
        
        
#lista o cursos que o aluno esta matriculado
def listar_cursos(id_usuario):
    # aqui eu usei o INNER JOIN para buscar cursos onde o aluno está matriculado
    cursor.execute("""
        SELECT cursos.id_curso, cursos.nome, cursos.horario
        FROM cursos
        INNER JOIN usuario_curso ON cursos.id_curso = usuario_curso.id_curso
        WHERE usuario_curso.id_usuario = ?
    """, (id_usuario,))

    #pega a busca e tranforma em uma varivel
    cursos = cursor.fetchall()

    #condiçao caso o aluno não esteja matriculado em nada
    if not cursos:
        print("\nNenhum curso encontrado para este aluno.")
        return

    print("\nCURSOS DISPONÍVEIS")
    #Percorre o banco de dados e mostra a coluna cursos que solicitei no inicio
    # [0] = id do curso, [1] = nome do curso  [2]] = horario do curso
    for curso in cursos:
        print(f"{curso[0]} - {curso[1]} - {curso[2]}")

    ids_validos = [curso[0] for curso in cursos]
    

    while True:
        #tratamento de erro para caso o aluno digite algo errado
        try:
            #variavel para a seleção do aluno e verifica se o ID digitado esta na lista 
            qualcurso = int(input("\nDigite o ID do curso para acessar a atividade: "))
            if qualcurso in ids_validos:
                acessar_atividades(qualcurso)
                break
            else:
                print("Curso Inválido. Escolha um curso da lista.")
        except ValueError:
            print("Digite apenas números.")
    
#busca quantas estrelas o aluno tem em um curso especifico
def buscar_estrelas(id_usuario):
#     #Aqui busca as estrelas totais do aluno com ID especifico
   cursor.execute("SELECT SUM(acerto) FROM usuario_atividade WHERE id_usuario = ?", (id_usuario,))
   resultado = cursor.fetchone()
   return resultado[0] if resultado else 0

#puxa a atividade do banco e imprimi na tela para ser respondida
def fazerAtividades(questoes):
    print(f"\n--- INICIANDO ATIVIDADES ---")
    
    #Percorre o banco de dados e transforma ele nas opções  
    for q in questoes:
        id_atividade, questao, A, B, C, D, gabarito, dica, id_curso = q
        
        print(f"\nQUESTÃO {id_atividade}: {questao}")
        print(f"A) {A}")
        print(f"B) {B}")
        print(f"C) {C}")
        print(f"D) {D}")

        #variavel para pedir dica
        usar_dica = input("Quer uma dica? (s/n): ").strip().lower()

        #condicional para o que foi escolhido pelo aluno
        if usar_dica == "s":
            print(f"Dica: {dica}") if dica else print("Esta questão não possui dica.")
        
        #Variavel para guardar resposta do aluno
        resposta = input("Qual sua resposta? (A/B/C/D): ").strip().upper()

        # Valida se o aluno digitou uma das letras permitidas
        if resposta in ['A', 'B', 'C', 'D']:
            
            
            # Comparação Direta: Letra digitada e Letra do Gabarito no banco
            if resposta == gabarito.strip().upper():

                ganhou = registrar_resposta(1, id_atividade)

                if ganhou:
                    print(f"⭐ BOA! Você acertou e ganhou uma estrela! (Total: {buscar_estrelas(1)})")
                else:
                    print("✅BOA! Você acertou - (Questão já respondida anteriormente)")
            else:
                #Aqui ele define que a letra digita e igual as letras do gabarito
                mapeamento = {'A': A, 'B': B, 'C': C, 'D': D}
                registrar_resposta_errada(1, id_atividade)
                print(f"❌ Errado. A resposta correta era a letra {gabarito} ({mapeamento[gabarito]})")
        else:
            print("⚠️ Opção inválida! Digite apenas A, B, C ou D.")

    # Exibi o resultado final para o aluno
    print("\n" + "="*30)
    print(f"FIM DA ATIVIDADE!")
    print(f"Agora voce tem {buscar_estrelas(1)} Estrelas")
    print("="*30)

#lista os cursos que o aluno esta matriculado na parte de progresso
def listar_cursos_progresso(id_usuario):
    cursor.execute("""
        SELECT c.id_curso, c.nome, c.horario
        FROM cursos c
        JOIN usuario_curso u ON c.id_curso = u.id_curso
        WHERE u.id_usuario = ?
    """, (id_usuario,))

    cursos = cursor.fetchall()

    if not cursos:
        print("\nVocê não está matriculado em nenhum curso.")
        return None

    print("\n SEUS CURSOS")

    for curso in cursos:
        print(f"{curso[0]} - {curso[1]} - {curso[2]}")

    try:
        id_curso = int(input("\nDigite o ID do curso: "))

        # garante que o curso pertence ao aluno
        ids_validos = [c[0] for c in cursos]

        if id_curso in ids_validos:
            return id_curso
        else:
            print("❌ Curso inválido.")
            return None

    except ValueError:
        print("❌ Digite apenas números.")
        return None