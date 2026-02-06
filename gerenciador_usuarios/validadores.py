import re

def formatar_cpf(cpf: str) -> str | None:
    numeros = re.sub(r"\D", "", cpf)

    if len(numeros) != 11:
        return None
    
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_email(email: str) -> bool:
    email = email.strip().lower()
    return bool(EMAIL_RE.match(email))
