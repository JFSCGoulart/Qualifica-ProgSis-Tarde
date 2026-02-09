import sqlite3

# Conectando ao banco de dados
from Connection.conexao import cursor, conexao

#reseta as atividades que foram marcadas como feita no banco de dados
def resetar_progresso(id_usuario):
    #Guardando a resposta do aluno
    resposta_p = input("Deseja realmente deletar seu progresso?(S/N) ").strip().upper()
    
    #Se resposta for S então ele muda se a tarefa vai contar pro ranking ou não 
    if resposta_p == "S":
        cursor.execute("""
        UPDATE usuario_atividade
        SET status = 0
        WHERE id_usuario = ?
    """, (id_usuario,))

        conexao.commit()
        print("⚠️ Progresso resetado!!.")

    elif resposta_p == "N":
        print("Operação cancelada!")

    else:
        print("Opção inválida!")
 
        
