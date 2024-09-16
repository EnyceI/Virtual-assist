import imaplib
import email
from  email.header import decode_header
username="xxx@gmail.com"
password="hidden"
#connect to Gmail's IMAP server
mail=imaplib.IMAP4_SSL("imap.gmail.com")
try:
    mail.login(username, password)
    print("Login successful")
except imaplib.IMAP4.error as e:
    print("Login failed:",e)
mail.select("Inbox")
status,message=mail.search(None,'ALL')

email_id=message[0].split()#lists of email ids
latest=email_id[-1]
res,msg=mail.fetch(latest,"(RFC822)")
#Parse the message content
for response in msg:
    msg=email.message_from_bytes(response[1])
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
    print("Subject:", subject)
    print("From:", msg.get("From"))

    # Check if the email message is multipart
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                print("Body:", body)
    else:
        body = msg.get_payload(decode=True).decode()
        print("Body:", body)

mail.logout()