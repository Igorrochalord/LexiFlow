import re


def validate_name(name: str) -> tuple[bool, str]:
    name = name.strip()
    if not name:
        return False, "Nome é obrigatório."
    if len(name) < 3:
        return False, "Nome deve ter pelo menos 3 caracteres."
    return True, ""


def validate_age(age_str: str) -> tuple[bool, str]:
    try:
        age = int(age_str.strip())
    except ValueError:
        return False, "Idade deve ser um número válido."
    if not (18 <= age <= 100):
        return False, "Idade deve ser entre 18 e 100 anos."
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    email = email.strip()
    if not email:
        return False, "Email corporativo é obrigatório para este plano."
    if not re.match(r"^[\w.+\-]+@[\w\-]+\.[\w.]{2,}$", email):
        return False, "Formato de email inválido."
    return True, ""
