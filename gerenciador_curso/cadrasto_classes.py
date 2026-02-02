class Professor:
    def __init__(self, nome, cpf, email, curso):
        self.nome = nome 
        self.cpf = cpf
        self.email = email
        self.curso = curso
    def __str__(self):
        return (f"--- Cadastro Professor ---\n"
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Email: {self.email}\n"
            f"Curso: {', '.join(self.curso) if self.curso else 'Nenhum curso'}\n")

class Aluno:
    def __init__(self, nome, cpf, email, curso):
        self.nome = nome 
        self.cpf = cpf
        self.email = email
        self.curso = curso
    def __str__(self):
        return (f"--- Cadastro Aluno ---\n"
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Email: {self.email}\n"
            f"Curso: {', '.join(self.curso) if self.curso else 'Nenhum curso'}\n")
class Coordenador:
    def __init__(self, nome, cpf, email):
        self.nome = nome 
        self.cpf = cpf
        self.email = email
    def __str__(self):
        return (f"--- Cadastro Coordenador---\n"
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Email: {self.email}\n"
        )