from progresso.menu_principal import rodar_menu_principal
from banco import criar_tabela

conexao = criar_tabela()
if __name__ == "__main__":
    try:
        rodar_menu_principal()
    finally:
        conexao.close()
