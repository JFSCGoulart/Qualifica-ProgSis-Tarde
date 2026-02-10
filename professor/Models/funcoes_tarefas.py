import sqlite3
conexao = sqlite3.connect('objetos.db')
cursor = conexao.cursor()


#Função usada para adicionar questoões

def adicionar_questao():
    contador = 0
    id_curso = input("Digite o id do curso correspondente: ")

    cursor.execute("SELECT 1 FROM cursos WHERE id_curso = ?", (id_curso,))
    procura = cursor.fetchone()

    if procura is None:
        print("O curso não existe.")
        return
    #O código acima válida se realmente existe um curso com o ID do input 

    quantidade_questoes = int(input("Quantas questões você deseja disponibilizar na tarefa? ")) 

    while contador < quantidade_questoes:
        questao = input("Digite o enunciado da questão: ")
        alternativa_a = input("Digite a alternativa A: ")
        alternativa_b = input("Digite a alternativa B: ")
        alternativa_c = input("Digite a alternativa C: ")
        alternativa_d = input("Digite a alternativa D: ")
        alternativa_certa = input("Digite a letra da alternativa certa (A/B/C/D): ").upper()
        dica = input("Digite a dica: ")

        cursor.execute("""
            INSERT INTO atividades
            (questao, A, B, C, D, gabarito, dica, id_curso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            questao, alternativa_a, alternativa_b,
            alternativa_c, alternativa_d,
            alternativa_certa, dica, id_curso
        ))

        conexao.commit()
        print("Questão adicionada")

        contador += 1
    
    #mostrar as questões
    cursor.execute("SELECT * FROM atividades WHERE id_curso = ?", (id_curso,))
    resultado = cursor.fetchall()

    for lista in resultado:
        print(f"{lista[0]}: {lista[1]}\n"
              f"A) {lista[2]}\n"
              f"B) {lista[3]}\n"
              f"C) {lista[4]}\n"
              f"D) {lista[5]}\n"
              f"Resposta: {lista[6]}\n"
              f"dica: {lista[7]}")

    print("As questões foram adicionadas com sucesso")
    

#Função usado para ver as questões cadastradas (usado no main)

def ver_questoes():
    id_curso = input("digite o id do curso correspondente: ")

    cursor.execute("SELECT 1 FROM cursos WHERE id_curso = ?", (id_curso,))
    procura = cursor.fetchone()

    if procura is None:
        print("o curso não existe, tente novamente")
    else:
        cursor.execute("SELECT * FROM atividades WHERE id_curso = ?", (id_curso,))
        resultado = cursor.fetchall()

        for lista in resultado:
            print(f"{lista[0]}: {lista[1]}\n"
                  f"A) {lista[2]}\n"
                  f"B) {lista[3]}\n"
                  f"C) {lista[4]}\n"
                  f"D) {lista[5]}\n"
                  f"Resposta: {lista[6]}\n"
                  f"dica: {lista[7]}")
    
    
#Função usada para ver tudo referente as atividades, conteúdo e questões (utilizada na funcão ver materia, presente no main)     

def ver_tudo():
    id_curso = int(input("digite o id do seu curso: "))

    cursor.execute("SELECT * FROM cursos WHERE id_curso = ?", (id_curso,))
    curso = cursor.fetchone()

    if curso is None:
        print("Não existe nenhum curso cadastrado.")
        return
    else:
        print(f"ID do curso: {curso[0]}\n"
              f"Nome do curso: {curso[1]}\n"
              f"Horário: {curso[2]}\n")

        cursor.execute("SELECT * FROM atividades WHERE id_curso = ?", (id_curso,))
        resultado = cursor.fetchall()

        for lista in resultado:
            print(f"{lista[0]}: {lista[1]}\n"
                  f"A) {lista[2]}\n"
                  f"B) {lista[3]}\n"
                  f"C) {lista[4]}\n"
                  f"D) {lista[5]}\n"
                  f"Resposta: {lista[6]}\n"
                  f"dica: {lista[7]}")
            

#Função usada para excluir questões!

def excluir_atividade():
    id_curso = input("digite o id do curso correspondente: ")

    cursor.execute("SELECT 1 FROM atividades WHERE id_curso = ?", (id_curso,))
    procura = cursor.fetchone()

    if procura is None:
        print("O curso não existe ou não há questões")
    else:
        #Else usado para mostrar as questões para o usuário escolher para excluir.
        cursor.execute("SELECT * FROM atividades WHERE id_curso = ?", (id_curso,))
        resultado = cursor.fetchall()

        for lista in resultado:
            print(f"{lista[0]}: {lista[1]}")

        while True:
            cursor.execute("SELECT 1 FROM atividades WHERE id_curso = ?", (id_curso,))
            if cursor.fetchone() is None:
                print("Não existe mais nenhuma questões")
                break

            id_atividade = int(input("digite o ID da atividade que você deseja excluir: "))

            cursor.execute("DELETE FROM atividades WHERE id_atividade = ?", (id_atividade,))
            conexao.commit()

            print("Questão apagada com sucesso.")

            escolha = input("Deseja apagar mais alguma questão?(s/n)").lower()
            if escolha == "n":
                break

                



          
       
        
    
            
