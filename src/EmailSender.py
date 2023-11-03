import smtplib
import json
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Message = json.load(open(config.MESSAGE_FILE_PATH))


class EmailSender:
    def __init__(self):
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.sender_email = config.FROM_EMAIL
        self.sender_password = config.MAIL_PASSWORD
        self.Users = config.USERS_MAIL

    def send_email_to_all(self, msg_code=99, town_id=0, page_num=0, err_msg=""):
        for user_mail in self.Users:
            email_subject = Message[str(msg_code)]["sub"].replace("{page_num}", str(page_num)).replace("{town_id}",
                                                                                                       str(town_id))
            email_message = Message[str(msg_code)]["msg"].replace("{page_num}", str(page_num)).replace("{town_id}",
                                                                                                       str(town_id)) + err_msg
            self._send_email(to_email=user_mail, subject=email_subject, message=email_message)
        print("------------------")

    def _send_email(self, to_email, subject, message):
        try:
            # Oluşturulan e-posta nesnesi
            email = MIMEMultipart()
            email['From'] = self.sender_email
            email['To'] = to_email
            email['Subject'] = subject

            # E-posta içeriği ekleniyor
            email.attach(MIMEText(message, 'plain'))

            # SMTP bağlantısı kuruluyor
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # SMTP bağlantısı başlatılıyor
                server.starttls()
                # SMTP server'a giriş yapılıyor
                server.login(self.sender_email, self.sender_password)
                # E-posta gönderiliyor
                server.sendmail(self.sender_email, to_email, email.as_string())

            print(f"Email was sent successfully. To:[{to_email}]")
        except Exception as e:
            print(f"E-posta gönderirken bir hata oluştu: {str(e)}")
