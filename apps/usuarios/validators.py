import re
from django.core.exceptions import ValidationError


def validar_senha(password):
    """Valida se a senha atende aos requisitos"""
    password = password.strip()  # Remove espaços no início e no final
    erros = []

    if " " in password:  # Impede espaços no meio
        erros.append("A senha não pode conter espaços em branco no meio.")

    if len(password) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres.")
    if not any(char.isupper() for char in password):
        erros.append("A senha deve conter pelo menos uma letra maiúscula.")
    if not any(char.isdigit() for char in password):
        erros.append("A senha deve conter pelo menos um número.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        erros.append("A senha deve conter pelo menos um caractere especial.")

    if erros:
        raise ValidationError(erros)
