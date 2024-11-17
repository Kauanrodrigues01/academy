from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMessage

def send_email(subject, message, to_email):
    email = EmailMessage(
        subject=subject,
        body=message,
        to=[to_email]
    )
    email.send()

def verify_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def is_valid_cpf(cpf):
    """Valida o CPF usando o algoritmo dos dígitos verificadores."""

    cpf = [int(digit) for digit in cpf]

    sum_1 = sum(cpf[i] * (10 - i) for i in range(9))
    digit_1 = (sum_1 * 10 % 11) % 10
    if digit_1 != cpf[9]:
        return False

    sum_2 = sum(cpf[i] * (11 - i) for i in range(10))
    digit_2 = (sum_2 * 10 % 11) % 10
    if digit_2 != cpf[10]:
        return False

    return True
