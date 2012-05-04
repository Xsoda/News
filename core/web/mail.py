import smtplib
import string

class Mail:
    def __init__(self, smtpserver, smtpport, fromAddress, fromPassword, subject):
        self.smtpserver = smtpserver
        self.smtpport = smtpport
        self.fromAddress = fromAddress
        self.fromPassword = fromPassword
        self.subject = subject

    def __call__(self, to, content):
        header = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (self.fromAddress, to, self.subject)
        msg = header + content
        mailserver = smtplib.SMTP(self.smtpserver, self.smtpport)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(self.fromAddress, self.fromPassword)
        mailserver.sendmail(self.fromAddress, to, msg)
        mailserver.close()
