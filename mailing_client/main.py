import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Secrets
from secrets import SENDER, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

# For gmail, need to enable `Allow Less Secure App Access`
# If you're using TLS, enter 587.
server = smtplib.SMTP('smtp.gmail.com', 587)

# Start the server
server.ehlo()

# Puts the connection to the SMTP server into TLS mode.
server.starttls()

# Login
server.login(SENDER_EMAIL, SENDER_PASSWORD)

# Construct Messages
msg = MIMEMultipart()
msg['From'] = SENDER
msg['To'] = RECEIVER_EMAIL
msg['Subject'] = 'Just a Test :)'

# Read message from a file
with open('message.txt', 'r') as f:
    message = f.read()

# Attach the message as plain text
msg.attach(MIMEText(message, 'plain'))

# Attachement files/payloads
filename = 'test_image.jpg'
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(p)


text = msg.as_string()
server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
