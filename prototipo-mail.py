from os import chdir, getcwd, listdir
from os.path import isfile
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configuração
host = 'smtp.gmail.com'
port = 587
user = 'email-here@gmail.com'
password = 'email-password-here'

# Criando objeto
print('Criando objeto servidor...')
server = smtplib.SMTP(host, port)

# Login com servidor
print('Login...')
server.ehlo()
server.starttls()
server.login(user, password)

# Diretório dos pdf
cam = 'F:\\GMAIL\\pdf\\'
# variáveis para lista de pdf e cpf com email
listaPdf = []
strCpfEmail = '{"08808624404":"ricardomelogomes.t@gmail.com","08808624405":"brunoreciprev@gmail.com"}'

listaCpf = json.loads(strCpfEmail)

# muda para o diretório dos pdf
chdir(cam)

# loop para adicionar os nomes dos pdf sem o ".pdf" no final
for c in listdir():
    if c.endswith('.pdf'):
        c = c[:-4]
        listaPdf.append(c)
        print("Enviar o arquivo: " + c + " para o email: " + listaCpf[c])

        # Criando mensagem
        message = 'Prezado beneficiário, segue em anexo o boleto do seu acordo.'
        print('Criando mensagem...')
        email_msg = MIMEMultipart()
        email_msg['From'] = user
        email_msg['To'] = listaCpf[c]
        email_msg['Subject'] = 'Reciprev - Boleto do acordo'
        print('Adicionando texto...')
        email_msg.attach(MIMEText(message, 'plain'))

        # obter arquivo
        print('Obtendo arquivo...')
        filename = c + ".pdf"
        filepath = cam + filename
        attachment = open(filepath, 'rb')

        print('Lendo arquivo...')
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)
        att.add_header('Content-Disposition', f'attachment; filename= {filename}')

        attachment.close()
        print('Adicionando arquivo ao email...')
        email_msg.attach(att)

        # Enviando mensagem
        print('Enviando mensagem...')
        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        print('Mensagem enviada!')

server.quit()
