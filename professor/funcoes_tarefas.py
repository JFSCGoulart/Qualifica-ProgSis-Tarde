import sqlite3
conexao=sqlite3.connect('objetos.db')
cursor=conexao.cursor()


#Função usada para adicionar questoões

def adicionar_questao():
    contador = 0
    numero_questao = 1
    id_conteudo = input("Digite o id do conteúdo correspondente: ")

    cursor.execute("SELECT 1 FROM conteudo WHERE id = ?", (id_conteudo,))
    procura = cursor.fetchone()
    mostrar = cursor.fetchall

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
        alternativa_certa = input("Digite a letra da alternativa certa: ")
        dica = input("Digite a dica: ")

        cursor.execute("""
            INSERT INTO questao
            (numero_questao, id_conteudo, enunciado, alternativa_a, alternativa_b,
             alternativa_c, alternativa_d, alternativa_certa, dica)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            numero_questao, id_conteudo, questao, alternativa_a,
            alternativa_b, alternativa_c, alternativa_d,
            alternativa_certa, dica
        ))

        conexao.commit()
        print("Questão adicionada")

        contador += 1
        numero_questao += 1
    
    #mostrar as questões
    cursor.execute("SELECT * FROM questao WHERE id_conteudo = ?", (id_conteudo,))
    resultado = cursor.fetchall()
    for lista in resultado:
        print(f"{lista[0]}: {lista[2]}\n"
            f"A) {lista[3]}\n"
            "B) {lista[4]}\n"
            f"C) {lista[5]}\n"
            f"D) {lista[6]}\n"
            f"Resposta: {lista[7]}\n"
            f"dica: {lista[8]}")
    print("As questões foram adicionadas com sucesso")
    

    
#Função usado para ver as questões cadastradas (usado no main)

def ver_questoes():
        id_conteudo = input("digite o id do conteudo que essa tarefa correspondente")
        cursor.execute("SELECT 1 FROM conteudo WHERE id = ?", (id_conteudo,))
        procura = cursor.fetchone()
        if procura is None:
            print("o curso não existe, tente novamente")
        else:
            cursor.execute("SELECT * FROM questao WHERE id_conteudo = ?", (id_conteudo,))
            resultado = cursor.fetchall()
            for lista in resultado:
                print(f"{lista[0]}: {lista[2]}\n"
                    f"A) {lista[3]}\n"
                    f"B) {lista[4]}\n"
                    f"C) {lista[5]}\n"
                    f"D) {lista[6]}\n"
                    f"Resposta: {lista[7]}\n"
                    f"dica: {lista[8]}")
    
    
#Função usada para ver tudo referente as atividades, conteúdo e questões (utilizada na funcão ver materia, presente no main)     

def ver_tudo():
    id_conteudo = int(input("digite o id do seu conteudo"))
    cursor.execute("SELECT 1 FROM conteudo WHERE id = ?", (id_conteudo,))
    resultado = cursor.fetchone()
    if resultado is None:
        print("Não existe nenhum curso seu cadastrado.")
        return
    else:
        cursor.execute("SELECT * FROM conteudo WHERE id = ?", (id_conteudo,))
        resultado = cursor.fetchall()
        for lista in resultado:
                print(f"ID do curso: {lista[0]}\n"
                    f"Título do curso: {lista[1]}\n"
                    f"Descrição do curso: {lista[2]}\n"
                    f"ID do professor: {lista[3]}\n"
                    f"Data de upload: {lista[4]}\n")
        
        cursor.execute("SELECT * FROM questao WHERE id_conteudo = ?", (id_conteudo,))
        resultado = cursor.fetchall()
        for lista in resultado:
                    print(f"{lista[0]}: {lista[2]}\n"
                        f"A) {lista[3]}\n"
                        f"B) {lista[4]}\n"
                        f"C) {lista[5]}\n"
                        f"D) {lista[6]}\n"
                        f"Resposta: {lista[7]}\n"
                        f"dica: {lista[8]}")
            
#Função usada para excluir questões!

def excluir_atividade():
    id_conteudo = input("digite o id do conteudo que essa tarefa correspondente")
    cursor.execute("SELECT 1 FROM questao WHERE id_conteudo = ?", (id_conteudo,))
    procura = cursor.fetchone()
    if procura is None:
            print("O curso não existe ou não há questões")
    else:
            #Else usado para mostrar as questões para o usuário escolher para excluir.
            cursor.execute("SELECT * FROM questao WHERE id_conteudo = ?", (id_conteudo,))
            resultado = cursor.fetchall()
            for lista in resultado:
                print(f"{lista[0]}: {lista[2]}\n"
                    f"A) {lista[3]}\n"
                    f"B) {lista[4]}\n"
                    f"C) {lista[5]}\n"
                    f"D) {lista[6]}\n"
                    f"Resposta: {lista[7]}\n"
                    f"dica: {lista[8]}")
            while True:
                cursor.execute("SELECT 1 FROM questao WHERE id_conteudo = ?", (id_conteudo,))
                if cursor.fetchone() is None:
                    print("Não existe mais nenhuma questões")
                    break
                numero_questao = int(input("digite o número da questão que você deseja excluir."))
                cursor.execute("DELETE FROM questao WHERE numero_questao = ? AND id_conteudo = ?", (numero_questao, id_conteudo))
                print("Questão apagada com sucesso.")
                conexao.commit()
                escolha = input("Deseja apagar mais alguma questão?(s/n)").lower()
                if escolha == "n":
                    break
                



          
       
        
    
            
