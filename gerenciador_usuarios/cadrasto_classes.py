from pwdlib import PasswordHash

# Instanciar um PasswordHash usando o método de classe recomendado.
password_hash = PasswordHash.recommended()

class Usuario:
    def __init__(self, senha_hash: str | None):
        self.senha_hash = senha_hash

    def verificar_senha(self, senha: str) -> bool:
        if not self.senha_hash:
            return False
        
        verified, new_hash = password_hash.verify_and_update(senha, self.senha_hash)

        if verified and new_hash:
            self.senha_hash = new_hash # Lembre de salvar esse novo hash no banco/arquivo depois do login, senão você perde o upgrade.

        return verified

class Pessoa(Usuario):
    def __init__(self, nome: str, email: str, cpf: str, senha: str, senha_confirmacao: str):
        self.nome = nome
        self.email = email
        self.cpf = cpf

        senha_hash = None
        if senha and senha == senha_confirmacao:
            senha_hash = password_hash.hash(senha)

        super().__init__(senha_hash)

class Professor(Pessoa):
    def __str__(self):
        return (
            f"--- Cadastro Professor ---\n"
            f"Nome: {self.nome}\n"
            f"Email: {self.email}\n"
            f"CPF: {self.cpf}\n"
        )

class Aluno(Pessoa):
    def __str__(self):
        return (
            f"--- Cadastro Aluno ---\n"
            f"Nome: {self.nome}\n"
            f"Email: {self.email}\n"
            f"CPF: {self.cpf}\n"
        )

class Coordenador(Pessoa):
    def __str__(self):
        return (
            f"--- Cadastro Coordenador ---\n"
            f"Nome: {self.nome}\n"
            f"Email: {self.email}\n"
            f"CPF: {self.cpf}\n"
        )
