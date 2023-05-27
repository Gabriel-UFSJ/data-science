import smtplib
from email.header import Header

class Agenda:
    def __init__(self):
        self.reunioes = []

    def criar_reuniao(self, data, horario, local, assunto, membros):
        reuniao = Reuniao(data, horario, local, assunto, membros)
        self.reunioes.append(reuniao)

        self.enviar_emails(reuniao)

        return reuniao

    def enviar_emails(self, reuniao):
        servidor_smtp = "smtp.gmail.com"
        porta_smtp = 587
        remetente = "milhasappemail@gmail.com"
        senha = "ezhrycothgfafqbm"

        server = smtplib.SMTP(servidor_smtp, porta_smtp)
        server.starttls()
        server.login(remetente, senha)

        assunto = f"Convite para Reunião - {reuniao.assunto}"
        corpo = f"""
        Olá,

        Você está convidado para a reunião sobre '{reuniao.assunto}' no dia {reuniao.data} às {reuniao.horario} no local {reuniao.local}.

        Atenciosamente,
        Milhas
        """

        for membro in reuniao.membros:
            destinatario = membro[1]
            mensagem = f"Subject: {assunto}\n\n{corpo}".encode('utf-8')
            server.sendmail(remetente, destinatario, mensagem)

        server.quit()


class Reuniao:
    def __init__(self, data, horario, local, assunto, membros):
        self.data = data
        self.horario = horario
        self.local = local
        self.assunto = assunto
        self.membros = membros