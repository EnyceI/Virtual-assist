import imaplib
import email
from email.header import decode_header
import  smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def email_read():

    username = "xxx@gmail.com"
    password = "xxx xxx xxx"
    # connect to Gmail's IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(username, password)
        print("Login successful")
    except imaplib.IMAP4.error as e:
        print("Login failed:", e)
    mail.select("Inbox")
    status, message = mail.search(None, 'ALL')

    email_id = message[0].split()  # lists of email ids
    latest = email_id[-1]
    res, msg = mail.fetch(latest, "(RFC822)")
    if res !="OK":
        print("Error fetching email")
    # Parse the message content
    for response in msg:
        if isinstance(response, tuple):
            # Extract and parse the email
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            print("Subject:", subject)
            print("From:", msg.get("From"))
            body=""

        # Check if the email message is multipart
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break

        else:
            body = msg.get_payload(decode=True).decode()
        print("Body:", body)

    mail.logout()
    # Create a reply message
    reply_msg= MIMEMultipart()
    reply_msg["From"]=username
    reply_msg["To"]="ppp@gmail.com"
    reply_msg["Subject"] = "Re: " + subject

    # Add the reply body
    body = "Thank you for your email! Have a great day ahead"
    reply_msg.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(username, password)
    smtp_server.sendmail(username, "ppp@gmail.com", reply_msg.as_string())
    smtp_server.quit()

email_read()
