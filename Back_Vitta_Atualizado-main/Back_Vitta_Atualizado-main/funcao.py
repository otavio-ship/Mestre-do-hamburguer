import re
import jwt
import datetime
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash


def validar_senha(senha):
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return "A senha precisa de pelo menos uma letra maiúscula."
    if not re.search(r"[0-9]", senha):
        return "A senha precisa de pelo menos um número."
    if not re.search(r"[@$!%*?&]", senha):
        return "A senha precisa de um caractere especial (@$!%*?&)."
    return None

def criptografar(senha):
    return generate_password_hash(senha)


def checar_senha(senha_plana, senha_hash):
    return check_password_hash(senha_hash, senha_plana)


def gerar_token(email):
    from main import app
    payload = {
        'id_usuario': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def remover_bearer(token):
    if token and token.startswith('Bearer '):
        return token.split(" ")[1]
    return token


import smtplib
from email.message import EmailMessage


def enviando_email(destinatario, assunto, corpo):
    try:
        email_origem = "ana.escudeiro5@gmail.com"
        senha_app = "knag jlld mnat hshf"

        msg = EmailMessage()
        msg.set_content(corpo)
        msg['Subject'] = assunto
        msg['From'] = email_origem
        msg['To'] = destinatario

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_origem, senha_app)
            smtp.send_message(msg)

        print(f"✅ SUCESSO: E-mail enviado para {destinatario}")
    except Exception as e:
        print(f" ERRO: {e}")