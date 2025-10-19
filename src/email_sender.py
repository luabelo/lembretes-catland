import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SMTP_SERVER, SMTP_PORT, EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO


def send_reminder_email(subject, message):
    if not all([EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO]):
        print("Erro: Credenciais de e-mail não configuradas no arquivo .env")
        return False

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"🐱 Catland - {subject}"
    
    body = f"""
    <html>
        <head></head>
        <body>
            <h2>Lembrete de Coordenação - Catland</h2>
            <p><strong>{subject}</strong></p>
            <p>{message}</p>
            <hr>
            <p><small>Este é um lembrete automático enviado pelo Sistema de Lembretes Catland.</small></p>
            <p><small>Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</small></p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
    
    return True
