def ranquear_alunos(lista_alunos, nome_curso):

    exibiu_menu = False
    ranking = sorted(lista_alunos, key=lambda estrelhas: estrelhas[2], reverse=True)
    
    for item in ranking:
        if item[1] == nome_curso:
            if not exibiu_menu:
                print(f"\n--- Total de acerto em {nome_curso} ---")
                exibiu_menu = True
            print(f"Nome: {item[0]} | Curso: {item[1]} | Estrelas: {item[2]} | Data: {item[3]}")
